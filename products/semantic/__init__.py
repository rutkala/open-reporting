"""
Open Reporting — Semantic Layer

Usage:
    from products import semantic

    # Query a measure
    df = semantic.query("unemployment_rate", domain="labour")
    df = semantic.query("unemployment_rate", domain="labour",
                        regions=["MAZOWIECKIE"], year_range=(2010, 2024))

    # Query a KPI
    df = semantic.query("unemployment_rate_yoy", domain="labour")

    # Get metadata
    m = semantic.get_measure("unemployment_rate", domain="labour")
    print(m.label, m.unit, m.direction)

    d = semantic.get_domain("labour")
    print(list(d.measures.keys()))
"""
from . import engine, loader
from .models import Domain, Measure, KPI


def get_domain(domain_id: str) -> Domain:
    """Return a loaded Domain object."""
    return loader.load(domain_id)


def get_measure(measure_id: str, domain: str) -> Measure:
    """Return a Measure definition by id."""
    return loader.load(domain).get_measure(measure_id)


def get_kpi(kpi_id: str, domain: str) -> KPI:
    """Return a KPI definition by id."""
    return loader.load(domain).get_kpi(kpi_id)


def query(
    metric_id: str,
    domain: str,
    group_by: list[str] | None = None,
    regions: list[str] | None = None,
    year_range: tuple[int, int] | None = None,
    year: int | None = None,
):
    """
    Query a measure or KPI by id.

    Automatically detects whether metric_id is a measure or KPI.
    Returns a pandas DataFrame.
    """
    d = loader.load(domain)

    if metric_id in d.measures:
        return engine.query_measure(
            d, metric_id,
            group_by=group_by,
            regions=regions,
            year_range=year_range,
            year=year,
        )

    if metric_id in d.kpis:
        return engine.query_kpi(
            d, metric_id,
            regions=regions,
            year_range=year_range,
            year=year,
        )

    raise KeyError(
        f"'{metric_id}' not found in domain '{domain}'. "
        f"Available measures: {list(d.measures.keys())}. "
        f"Available KPIs: {list(d.kpis.keys())}."
    )


def list_measures(domain: str) -> list[Measure]:
    return list(loader.load(domain).measures.values())


def list_kpis(domain: str) -> list[KPI]:
    return list(loader.load(domain).kpis.values())
