"""
Shared rate-limiter and HTTP helper for GUS API extractors (BDL, DBW).

Usage:
    limiter = WeeklyRateLimiter("bdl", 50_000, state_path, min_interval_s=0.15)
    data = get_json(session, url, params, limiter)
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

import requests

logger = logging.getLogger(__name__)


class BudgetExhausted(Exception):
    pass


class FetchSkip(Exception):
    pass


class FetchAbort(Exception):
    pass


def _iso_week(dt: datetime) -> str:
    return dt.strftime("%G-W%V")


def _atomic_write(path: Path, data: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


class WeeklyRateLimiter:
    def __init__(
        self,
        name: str,
        weekly_cap: int,
        state_path: Path,
        min_interval_s: float = 0.25,
        reserve: int = 200,
    ):
        self.name = name
        self.weekly_cap = weekly_cap
        self.state_path = state_path
        self.min_interval_s = min_interval_s
        self.reserve = reserve
        self._last_request_ts: float = 0.0
        self._used_this_run: int = 0
        self._state = self._load()

    def _load(self) -> dict:
        if self.state_path.exists():
            try:
                return json.loads(self.state_path.read_text())
            except Exception:
                pass
        return {"week": "", "used": 0, "header_remaining": self.weekly_cap,
                "header_reset": "", "updated_at": ""}

    def _save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(self.state_path, self._state)

    def _maybe_reset_week(self) -> None:
        now = datetime.now(timezone.utc)
        current_week = _iso_week(now)
        if self._state["week"] != current_week:
            logger.info(f"[{self.name}] New week {current_week} — resetting counter")
            self._state["week"] = current_week
            self._state["used"] = 0
            self._save()

    @property
    def remaining(self) -> int:
        local = self.weekly_cap - self._state.get("used", 0)
        header = self._state.get("header_remaining", self.weekly_cap)
        return min(local, header)

    @property
    def used_this_run(self) -> int:
        return self._used_this_run

    def acquire(self) -> None:
        self._maybe_reset_week()
        if self.remaining <= self.reserve:
            raise BudgetExhausted(
                f"[{self.name}] Weekly budget exhausted "
                f"(remaining={self.remaining}, reserve={self.reserve})"
            )
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < self.min_interval_s:
            time.sleep(self.min_interval_s - elapsed)
        self._state["used"] = self._state.get("used", 0) + 1
        self._used_this_run += 1
        self._last_request_ts = time.monotonic()
        if self._state["used"] % 50 == 0:
            self._save()

    def update_from_headers(self, headers: Mapping) -> None:
        remaining_hdr = headers.get("X-Rate-Limit-Remaining")
        reset_hdr = headers.get("X-Rate-Limit-Reset", "")
        if remaining_hdr is not None:
            try:
                hdr_val = int(remaining_hdr)
                if hdr_val < self._state.get("header_remaining", self.weekly_cap):
                    self._state["header_remaining"] = hdr_val
                    self._state["header_reset"] = reset_hdr
                    self._save()
            except ValueError:
                pass

    def sleep_until_reset(self) -> None:
        reset_str = self._state.get("header_reset", "")
        wait = 60.0
        if reset_str:
            try:
                reset_dt = datetime.fromisoformat(reset_str.replace("Z", "+00:00"))
                wait = max(1.0, (reset_dt - datetime.now(timezone.utc)).total_seconds())
            except Exception:
                pass
        wait = min(wait, 300.0)
        logger.warning(f"[{self.name}] Rate limited — sleeping {wait:.0f}s")
        time.sleep(wait)


def get_json(
    session: requests.Session,
    url: str,
    params: dict,
    limiter: WeeklyRateLimiter,
    max_attempts: int = 4,
) -> dict | list:
    attempt = 0
    rate_limited_once = False
    while True:
        limiter.acquire()
        try:
            resp = session.get(url, params=params, timeout=30)
            limiter.update_from_headers(resp.headers)

            if resp.status_code == 429:
                if not rate_limited_once:
                    rate_limited_once = True
                    limiter.sleep_until_reset()
                    continue
                else:
                    raise BudgetExhausted(f"429 on {url} after reset sleep")

            if resp.status_code in (401, 403):
                raise FetchAbort(f"HTTP {resp.status_code} on {url} — check API key")

            if resp.status_code in (400, 404):
                raise FetchSkip(f"HTTP {resp.status_code} on {url}")

            if resp.status_code >= 500:
                raise requests.HTTPError(f"HTTP {resp.status_code}", response=resp)

            resp.raise_for_status()
            return resp.json()

        except (FetchSkip, FetchAbort, BudgetExhausted):
            raise
        except Exception as e:
            attempt += 1
            if attempt >= max_attempts:
                raise FetchSkip(f"Failed after {max_attempts} attempts on {url}: {e}") from e
            wait = 2 ** attempt
            logger.warning(f"[{limiter.name}] {e} — retry {attempt}/{max_attempts} in {wait}s")
            time.sleep(wait)
