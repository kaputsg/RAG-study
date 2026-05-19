from app.deepseek_client import deepseek_client


def main():
    # 这段内容模拟“从知识库里检索出来的资料”
    context = """
RAG 是 Retrieval-Augmented Generation 的缩写，中文叫检索增强生成。
它的基本流程是：先根据用户问题从知识库中检索相关资料，
然后把检索到的资料和用户问题一起交给大模型，
最后由大模型根据资料生成答案。

RAG 的主要作用是让大模型可以回答私有知识库中的问题，
也可以减少模型胡编乱造的问题。
"""

    question = "RAG 的基本流程是什么？"

    system_prompt = """
你是一个严格的知识库问答助手。
你只能根据提供的资料回答问题。
如果资料中没有答案，请回答：我没有在知识库中找到相关信息。
不要使用资料以外的知识。
回答要简洁清楚。
"""

    user_prompt = f"""
下面是知识库资料：

{context}

用户问题：
{question}
"""

    answer = deepseek_client.chat(
        user_message=user_prompt,
        system_message=system_prompt,
        temperature=0.2,
        max_tokens=800
    )

    print("模型回答：")
    print(answer)


if __name__ == "__main__":
    main()