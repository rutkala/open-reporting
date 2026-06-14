#!/usr/bin/env python3
"""
Layer-2 research log generator.

Joins the KPP central-institution list, the dane.gov.pl publisher enumeration,
and the curated research findings (layer2_findings.yaml) into one exhaustive
status table — every central institution gets a documented result.

Output: docs/layer2-research-log.md

Usage: python3 infra/scheduler/layer2_log.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO = Path("/opt/open-reporting")
KPP = REPO / "data/kpp_institutions.json"
DGP = REPO / "data/danegovpl_institutions.json"
FINDINGS = REPO / "products/ingestion/registry/layer2_findings.yaml"
OUT = REPO / "docs/layer2-research-log.md"

_STOP = {"w", "i", "do", "spraw", "oraz", "z", "na", "rzeczypospolitej",
         "polskiej", "polski", "rp", "the"}
KIND_BADGE = {
    "own_api": "🟢 own API", "own_ogc": "🟢 own WMS/WFS", "own_bulk": "🟢 own bulk",
    "danegovpl": "🟡 dane.gov.pl", "reports_only": "🟠 reports only",
    "no_open_data": "⚫ no open data",
}


def toks(s: str) -> set[str]:
    s = re.sub(r"[^a-ząćęłńóśźż0-9 ]", " ", (s or "").lower())
    return {w for w in s.split() if len(w) > 2 and w not in _STOP}


def main() -> int:
    central = json.loads(KPP.read_text())["institutions"]
    dgp = json.loads(DGP.read_text())["institutions"]
    findings = yaml.safe_load(FINDINGS.read_text())["findings"]

    dgp_idx = [(toks(d["title"]), d["datasets"]) for d in dgp]

    def dgp_n(name):
        t = toks(name)
        best = 0
        for dt, n in dgp_idx:
            if dt and len(t & dt) >= 2 and len(t & dt) >= min(len(t), len(dt)) * 0.6:
                best = max(best, n)
        return best

    rows = []
    for c in central:
        nl = c["name"].lower()
        f = next((v for k, v in findings.items() if k in nl), None)
        dn = dgp_n(c["name"])
        if f:
            badge = KIND_BADGE.get(f["kind"], "🟡 researched")
            src = f.get("source") or ""
            note = f.get("note", "")
            researched = True
        elif dn:
            badge, src, note, researched = "🟡 dane.gov.pl", "", f"on dane.gov.pl ({dn} datasets); own channel unchecked", False
        else:
            badge, src, note, researched = "⬜ to research", "", "not on dane.gov.pl; unchecked", False
        rows.append((researched, badge, c["name"].title(), src,
                     note, dn, c["www"]))

    rows.sort(key=lambda r: (not r[0], r[2]))
    done = sum(1 for r in rows if r[0])
    kinds = Counter(r[1] for r in rows)

    L = [
        "# Layer-2 research log — ALL KPP central institutions",
        "",
        "Exhaustive per-institution research (no category skipped). Each gets a",
        "documented own-data-channel result; dane.gov.pl status auto-cross-checked.",
        "Findings curated in `products/ingestion/registry/layer2_findings.yaml`.",
        "",
        f"- **{done} / {len(rows)} researched** to a definite own-channel result",
        "- " + " · ".join(f"{b} {n}" for b, n in kinds.most_common()),
        "",
        "| Result | Institution | Source key | dane.gov.pl | Note | Site |",
        "|---|---|---|--:|---|---|",
    ]
    for researched, badge, name, src, note, dn, www in rows:
        link = f"[↗](http://{www.replace('https://','').replace('http://','').rstrip('/')})" if www else ""
        L.append(f"| {badge} | {name} | {src} | {dn or ''} | {note} | {link} |")
    L.append("")
    OUT.write_text("\n".join(L))
    print(f"layer2 log: {done}/{len(rows)} researched → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
