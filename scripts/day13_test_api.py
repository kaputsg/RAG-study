"""
Day 13: API smoke test script.

Run prerequisites:
1. Start backend first:
   python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
2. Then run:
   python -m scripts.day13_test_api
   python -m scripts.day13_eval_questions
"""

import json
import tempfile
from pathlib import Path
from urllib.parse import quote

import requests


BASE_URL = "http://127.0.0.1:8000"
TEMP_FILENAME = "day13_temp_test.txt"
TEMP_CONTENT = (
    "Day 13 临时测试文档。\n"
    "这个文档用于测试上传接口和删除接口。\n"
    "删除成功后它不应该继续出现在知识库列表中。"
)


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_response(api_name, response):
    print(f"接口：{api_name}")
    print(f"状态码：{response.status_code}")

    try:
        data = response.json()
        print("返回 JSON：")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except ValueError:
        print("返回内容不是 JSON：")
        print(response.text)


def print_request_error(api_name, error):
    print(f"接口：{api_name}")
    print(f"请求失败：{error}")


def test_health():
    print_section("test_health: GET /health")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        print_response("GET /health", response)
    except requests.RequestException as error:
        print_request_error("GET /health", error)


def test_documents():
    print_section("test_documents: GET /documents")

    try:
        response = requests.get(f"{BASE_URL}/documents", timeout=30)
        print_response("GET /documents", response)
    except requests.RequestException as error:
        print_request_error("GET /documents", error)


def test_ask_known():
    print_section("test_ask_known: POST /ask")
    payload = {
        "question": "开发 Python 后端 API 接口服务推荐用什么框架？"
    }

    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=60)
        print_response("POST /ask known", response)
    except requests.RequestException as error:
        print_request_error("POST /ask known", error)


def test_ask_unknown():
    print_section("test_ask_unknown: POST /ask")
    payload = {
        "question": "数据库事务的 ACID 是什么？"
    }

    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=60)
        print_response("POST /ask unknown", response)
    except requests.RequestException as error:
        print_request_error("POST /ask unknown", error)


def test_upload_temp_document():
    print_section("test_upload_temp_document: POST /documents/upload")

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / TEMP_FILENAME
            temp_path.write_text(TEMP_CONTENT, encoding="utf-8")

            with temp_path.open("rb") as file:
                files = {
                    "file": (TEMP_FILENAME, file, "text/plain")
                }
                response = requests.post(
                    f"{BASE_URL}/documents/upload",
                    files=files,
                    timeout=60
                )

        print_response("POST /documents/upload", response)
    except requests.RequestException as error:
        print_request_error("POST /documents/upload", error)
    except OSError as error:
        print_request_error("create temp upload file", error)


def test_delete_temp_document():
    print_section("test_delete_temp_document: DELETE /documents/{filename}")
    encoded_filename = quote(TEMP_FILENAME)

    try:
        response = requests.delete(
            f"{BASE_URL}/documents/{encoded_filename}",
            timeout=60
        )
        print_response("DELETE /documents/{filename}", response)
    except requests.RequestException as error:
        print_request_error("DELETE /documents/{filename}", error)


def main():
    test_health()
    test_documents()
    test_ask_known()
    test_ask_unknown()
    test_upload_temp_document()
    test_delete_temp_document()
    test_documents()


if __name__ == "__main__":
    main()
