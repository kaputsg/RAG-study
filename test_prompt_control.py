from app.deepseek_client import deepseek_client


def test_normal_prompt():
    """
    普通提示词测试。
    模型会根据自己的知识回答。
    """

    system_prompt = """
你是一个专业的 AI 助手。
请用中文回答用户问题。
"""

    question = "请介绍一下 RAG 的作用。"

    answer = deepseek_client.chat(
        user_message=question,
        system_message=system_prompt,
        temperature=0.2,
        max_tokens=800
    )

    print("===== 普通提示词回答 =====")
    print(answer)


def test_strict_prompt():
    """
    严格提示词测试。
    模拟未来 RAG 项目中的回答规则。
    """

    system_prompt = """
你是一个严格的知识库问答助手。
你只能根据用户提供的资料回答问题。
如果用户没有提供资料，你必须回答：我没有在知识库中找到相关信息。
不要根据自己的知识补充答案。
"""

    question = "请介绍一下 RAG 的作用。"

    answer = deepseek_client.chat(
        user_message=question,
        system_message=system_prompt,
        temperature=0.2,
        max_tokens=800
    )

    print("===== 严格提示词回答 =====")
    print(answer)


if __name__ == "__main__":
    test_normal_prompt()
    print()
    test_strict_prompt()