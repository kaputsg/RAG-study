"""
Day 13: Basic RAG evaluation script.

Run prerequisites:
1. Start backend first:
   python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
2. Then run:
   python -m scripts.day13_test_api
   python -m scripts.day13_eval_questions
"""

import json
from pathlib import Path

import requests


BASE_URL = "http://127.0.0.1:8000"
EVAL_FILE = Path(__file__).resolve().parents[1] / "data" / "eval_questions.json"


def load_questions():
    with EVAL_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def contains_any_keyword(answer, expected_keywords):
    if not expected_keywords:
        return True

    return any(keyword in answer for keyword in expected_keywords)


def ask_question(question):
    response = requests.post(
        f"{BASE_URL}/ask",
        json={"question": question},
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def print_result(result):
    print("\n" + "-" * 70)
    print(f"id: {result['id']}")
    print(f"question: {result['question']}")
    print(f"expected_hit: {result['expected_hit']}")
    print(f"actual_hit: {result['actual_hit']}")
    print(f"confidence: {result['confidence']}")
    print(f"max_score: {result['max_score']}")
    print(f"keyword_pass: {result['keyword_pass']}")
    print(f"hit_pass: {result['hit_pass']}")
    print(f"pass: {result['pass']}")
    print(f"answer_120: {result['answer_120']}")


def evaluate_item(item):
    try:
        data = ask_question(item["question"])
        answer = data.get("answer", "")
        retrieval_info = data.get("retrieval_info", {})
        actual_hit = bool(retrieval_info.get("hit", False))
        max_score = retrieval_info.get("max_score", 0)
        confidence = retrieval_info.get("confidence", "low")
        source_count = retrieval_info.get("source_count", 0)

        keyword_pass = contains_any_keyword(
            answer,
            item.get("expected_keywords", [])
        )
        hit_pass = actual_hit == item.get("expected_hit")
        passed = keyword_pass and hit_pass

        return {
            "id": item.get("id", ""),
            "question": item.get("question", ""),
            "expected_hit": item.get("expected_hit"),
            "actual_hit": actual_hit,
            "retrieval_info": retrieval_info,
            "max_score": max_score,
            "confidence": confidence,
            "source_count": source_count,
            "keyword_pass": keyword_pass,
            "hit_pass": hit_pass,
            "pass": passed,
            "answer_120": answer[:120]
        }
    except requests.RequestException as error:
        return {
            "id": item.get("id", ""),
            "question": item.get("question", ""),
            "expected_hit": item.get("expected_hit"),
            "actual_hit": None,
            "retrieval_info": {},
            "max_score": 0,
            "confidence": "request_failed",
            "source_count": 0,
            "keyword_pass": False,
            "hit_pass": False,
            "pass": False,
            "answer_120": f"请求失败：{error}"
        }


def main():
    questions = load_questions()
    results = []

    print(f"读取评估问题集：{EVAL_FILE}")
    print(f"问题数量：{len(questions)}")

    for item in questions:
        result = evaluate_item(item)
        results.append(result)
        print_result(result)

    total = len(results)
    passed = sum(1 for result in results if result["pass"])
    failed = total - passed
    pass_rate = passed / total if total else 0

    print("\n" + "=" * 70)
    print("汇总")
    print("=" * 70)
    print(f"total: {total}")
    print(f"passed: {passed}")
    print(f"failed: {failed}")
    print(f"pass_rate: {pass_rate:.2%}")


if __name__ == "__main__":
    main()
