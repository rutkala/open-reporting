"""
Loads domain YAML files into Domain model objects.
"""
import logging
from pathlib import Path

import yaml

from .models import Domain, Fact, Dimension, Measure, KPI, Section

log = logging.getLogger(__name__)

DOMAINS_DIR = Path(__file__).parent

_cache: dict[str, Domain] = {}


def load(domain_id: str) -> Domain:
    """Load a domain by id, with in-process caching."""
    if domain_id in _cache:
        return _cache[domain_id]

    path = DOMAINS_DIR / domain_id / "model.yml"
    if not path.exists():
        raise FileNotFoundError(f"Domain file not found: {path}")

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    domain = _parse(raw)
    _cache[domain_id] = domain
    log.debug("Loaded domain '%s' from %s", domain_id, path)
    return domain


def load_all() -> dict[str, Domain]:
    """Load all domain YAML files from the domains directory."""
    domains = {}
    for path in DOMAINS_DIR.glob("*/model.yml"):
        domain_id = path.parent.name
        domains[domain_id] = load(domain_id)
    return domains


def _parse(raw: dict) -> Domain:
    facts = {
        f["id"]: Fact(
            id=f["id"],
            schema=f["schema"],
            table=f["table"],
            grain=f["grain"],
        )
        for f in raw.get("facts", [])
    }

    dimensions = {
        d["id"]: Dimension(
            id=d["id"],
            column=d["column"],
            label=d["label"],
            type=d["type"],
        )
        for d in raw.get("dimensions", [])
    }

    measures = {
        m["id"]: Measure(
            id=m["id"],
            label=m["label"],
            column=m["column"],
            fact=m["fact"],
            aggregation=m["aggregation"],
            unit=m["unit"],
            direction=m["direction"],
            description=m.get("description", ""),
        )
        for m in raw.get("measures", [])
    }

    kpis = {
        k["id"]: KPI(
            id=k["id"],
            label=k["label"],
            base_measure=k["base_measure"],
            calculation=k["calculation"],
            unit=k["unit"],
            description=k.get("description", ""),
        )
        for k in raw.get("kpis", [])
    }

    sections = [
        Section(
            id=s["id"],
            label=s["label"],
            measures=s["measures"],
        )
        for s in raw.get("sections", [])
    ]

    return Domain(
        id=raw["domain"],
        label=raw["label"],
        description=raw.get("description", ""),
        facts=facts,
        dimensions=dimensions,
        measures=measures,
        kpis=kpis,
        sections=sections,
    )
