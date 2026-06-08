#!/usr/bin/env python3
import logging
import os

import duckdb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv(override=True)
logger = logging.getLogger(__name__)

app = FastAPI(title="Conversational Data API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _db() -> duckdb.DuckDBPyConnection:
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)


class QuestionRequest(BaseModel):
    question: str


def mock_llm_sql_generator(question: str) -> str:
    """Mock LLM function that generates a DuckDB SQL query based on the question."""
    q = question.lower()
    if "inflation" in q:
        return "SELECT 5.4 AS answer"
    elif "gdp" in q:
        return "SELECT 100.5 AS answer"
    else:
        return "SELECT 42.0 AS answer"


@app.post("/ask")
def ask_question(request: QuestionRequest) -> dict:
    try:
        sql_query = mock_llm_sql_generator(request.question)
        logger.info(f"Generated SQL: {sql_query}")
        
        with _db() as conn:
            result = conn.execute(sql_query).fetchone()
            
        if not result:
            raise HTTPException(status_code=404, detail="No answer returned from query.")
            
        return {"answer": float(result[0])}
    except duckdb.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
