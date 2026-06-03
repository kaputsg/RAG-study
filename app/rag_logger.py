"""
Simple JSONL logger for RAG ask requests.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "rag_requests.jsonl"


def _compact_sources(sources):
    compact_sources = []

    for source in sources:
        compact_sources.append({
            "source": source.get("source", ""),
            "chunk_index": source.get("chunk_index", 0),
            "score": source.get("score", 0)
        })

    return compact_sources


def write_rag_log(
    question: str,
    answer: str,
    retrieval_info: dict,
    sources: list,
    success: bool,
    error: str | None = None
) -> None:
    """
    Append one RAG request log line. Logging failures must not affect /ask.
    """

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        log_item = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "answer": answer,
            "retrieval_info": retrieval_info,
            "sources": _compact_sources(sources),
            "success": success,
            "error": error
        }

        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(log_item, ensure_ascii=False) + "\n")
    except Exception as exc:
        print(f"Failed to write RAG log: {exc}")
