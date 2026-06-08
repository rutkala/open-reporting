#!/usr/bin/env python3
"""
Phase 4: Data-as-a-Service Mock GraphQL API.
Allows B2B users to query metrics directly from the DuckDB warehouse.
"""
import os
import re
import logging
from typing import Optional, Dict, Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import duckdb
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="B2B GraphQL-like Data API")
VALID_API_KEY = os.environ.get("B2B_API_KEY", "secret-b2b-key")


def _db() -> duckdb.DuckDBPyConnection:
    """Returns a DuckDB connection using the warehouse path from env."""
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path, read_only=True)


class GraphQLQuery(BaseModel):
    query: str
    variables: Optional[Dict[str, Any]] = None


def _fetch_metric(
    conn: duckdb.DuckDBPyConnection, table: str, col: str, year: Optional[int]
) -> list:
    """Fetches a specific metric from the given curated table."""
    sql = f"SELECT period_year, {col} FROM curated.{table} WHERE geo = 'PL'"
    params = []
    if year is not None:
        sql += " AND period_year = ?"
        params.append(year)
    sql += " ORDER BY period_year DESC LIMIT 10"
    
    return conn.execute(sql, params).df().to_dict(orient="records")


def parse_mock_graphql(query: str) -> Dict[str, Any]:
    """Mock parser that returns data based on keywords in the query string."""
    q = query.lower()
    res = {}

    try:
        conn = _db()
    except Exception as e:
        logger.error(f"Failed to connect to DuckDB: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        # Extract optional year filter, e.g. "year: 2022"
        year_match = re.search(r'year:\s*(\d+)', q)
        year = int(year_match.group(1)) if year_match else None

        if "inflation" in q:
            res["inflation"] = _fetch_metric(
                conn, "fact_prices_overview", "inflation_rate_pct", year
            )

        if "gdp" in q:
            res["gdp"] = _fetch_metric(
                conn, "fact_macro_overview", "gdp_real_growth_pct", year
            )

    except Exception as e:
        logger.error(f"Error executing mock GraphQL query: {e}")
        raise HTTPException(status_code=500, detail="Error executing query")
    finally:
        conn.close()

    return {"data": res}


@app.post("/graphql")
def graphql_endpoint(
    req: GraphQLQuery,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """GraphQL-like endpoint requiring X-API-Key."""
    if not x_api_key or x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not req.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    return parse_mock_graphql(req.query)


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
