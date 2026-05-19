from app.deepseek_client import deepseek_client


def main():
    system_prompt = """
你是一个专业的 AI 大模型应用开发老师。
请用中文回答。
回答要清楚、具体，不要说空话。
"""

    question = "请用通俗的话解释什么是 RAG。"

    answer = deepseek_client.chat(
        user_message=question,
        system_message=system_prompt,
        temperature=0.2,
        max_tokens=800,
        show_model_name=True
    )

    print("模型回答：")
    print(answer)


if __name__ == "__main__":
    main()