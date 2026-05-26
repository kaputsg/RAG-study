"""
Day 7：测试 FastAPI RAG 接口

目标：
1. 用 Python requests 调用 /health
2. 用 Python requests 调用 /ask
3. 测试正常问题、无答案问题、空问题
"""

import json
import requests


BASE_URL = "http://127.0.0.1:8000"


def test_health():
    """
    测试 /health 接口。
    """

    # TODO 1：发送 GET 请求到 /health
    # 提示：response = requests.get(f"{BASE_URL}/health")

    # TODO 2：打印状态码

    # TODO 3：打印 JSON 返回结果
    response = requests.get(f"{BASE_URL}/health")

    print("状态码：", response.status_code)
    print("返回结果：")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


def test_ask(question):
    """
    测试 /ask 接口。
    """

    # TODO 1：准备请求体 payload
    # 格式：{"question": question}

    # TODO 2：发送 POST 请求到 /ask
    # 提示：requests.post(f"{BASE_URL}/ask", json=payload)

    # TODO 3：打印问题

    # TODO 4：打印状态码

    # TODO 5：尝试打印 JSON 返回结果

    payload = {
        "question": question
    }

    response = requests.post(
        f"{BASE_URL}/ask",
        json=payload
    )

    print("问题：", question)
    print("状态码：", response.status_code)
    print("返回结果：", response.json())


def main():
    test_health()

    print("\n" + "=" * 50)
    test_ask("开发 Python 后端 API 接口服务推荐用什么框架？")

    print("\n" + "=" * 50)
    test_ask("数据库事务的 ACID 是什么？")

    print("\n" + "=" * 50)
    test_ask("   ")


if __name__ == "__main__":
    main()
