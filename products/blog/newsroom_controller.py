#!/usr/bin/env python3
"""
Newsroom Controller Pipeline.

Acts as the pipeline between anomaly_detector.py and ghost_publisher.py.
Takes a JSON payload representing a data anomaly, generates an article via LLM,
and publishes it as a draft to Ghost.
"""

import argparse
import json
import logging
import sys
from typing import Any, Dict

from products.blog.ghost_publisher import create_draft_post

logger = logging.getLogger(__name__)


def mock_llm_call(prompt: str) -> str:
    """
    Mock the LLM call to return a hardcoded markdown string.
    Placeholder until an actual LLM library is integrated.
    """
    logger.info("Mocking LLM call with prompt (length: %d chars)...", len(prompt))
    return """# Nagły Wzrost Wskaźników: Co Mówią Dane?

Dzisiejsze dane pokazują interesujące odchylenia od normy. Zespół Open Reporting 
stale monitoruje sytuację i analizuje najnowsze odczyty.

## Szczegóły Anomalii

Zanotowaliśmy niespodziewaną zmianę, która wymaga szerszego kontekstu. 
Z-score wskazuje na istotność statystyczną zjawiska, wykraczając poza standardowe 
wahania sezonowe. Będziemy przyglądać się, czy to jednorazowy wyskok, czy 
początek nowego trendu.

*Więcej szczegółów wkrótce w pełnym raporcie analitycznym.*
"""


def generate_prompt(anomaly: Dict[str, Any]) -> str:
    """
    Format a prompt instructing an LLM to act as a Polish Data Journalist.
    """
    metric = anomaly.get("metric", "Nieznana Metryka")
    val = anomaly.get("value", 0.0)
    mean = anomaly.get("historical_mean", 0.0)
    z_score = anomaly.get("z_score", 0.0)

    prompt = (
        "Jesteś polskim dziennikarzem danych (Polish Data Journalist). "
        "Napisz artykuł na około 500 słów w formacie Markdown, "
        "wyjaśniający poniższą anomalię w danych analitycznych:\n\n"
        f"Metryka: {metric}\n"
        f"Wartość obecna: {val}\n"
        f"Średnia historyczna: {mean}\n"
        f"Z-score: {z_score}\n\n"
        "Skup się na przystępnym wytłumaczeniu zjawiska dla czytelników "
        "niebędących ekspertami od statystyki."
    )
    return prompt


def process_anomaly(anomaly_json: str) -> None:
    """
    Process an anomaly JSON and publish a draft article to Ghost.
    """
    try:
        anomaly = json.loads(anomaly_json)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse anomaly JSON: %s", e)
        raise ValueError("Invalid anomaly JSON provided.") from e

    metric = anomaly.get("metric", "Nieznana Metryka")

    logger.info("Processing anomaly for metric: %s", metric)

    # 1. Format LLM prompt
    prompt = generate_prompt(anomaly)

    # 2. Call LLM (mocked) to get article content
    markdown_content = mock_llm_call(prompt)

    # 3. Publish to Ghost CMS as a draft
    title = f"Alert Danych: Zmiana w metryce {metric}"
    tags = ["anomalie", "dane"]

    try:
        post_id = create_draft_post(title=title, markdown_content=markdown_content, tags=tags)
        logger.info("Successfully created draft post for '%s' (ID: %s)", metric, post_id)
    except Exception as e:
        logger.error("Failed to publish draft to Ghost: %s", e)
        raise


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    
    parser = argparse.ArgumentParser(description="Newsroom Controller Pipeline")
    parser.add_argument(
        "--anomaly",
        type=str,
        required=True,
        help='JSON string representing the anomaly (e.g. {"metric": "Infl", "value": 1.2})'
    )

    args = parser.parse_args()

    try:
        process_anomaly(args.anomaly)
    except Exception as e:
        logger.error("Pipeline execution failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
