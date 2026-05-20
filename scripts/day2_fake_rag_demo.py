from app.deepseek_client import deepseek_client

from scripts.day2_fake_vector_search import (
    raw_documents,
    text_to_fake_vector,
    build_documents,
    search
)

def main():
    """
    最小 RAG Demo：
    1. 构建带向量的文档列表
    2. 把用户问题转成假向量
    3. 检索最相关资料
    4. 把资料和问题交给 DeepSeek
    5. 打印模型回答
    """

    question = "数据库事务的 ACID 是什么？"

    # TODO 1：用 build_documents(raw_documents) 得到 documents
    documents = build_documents(raw_documents)

    # TODO 2：用 text_to_fake_vector(question) 得到 question_vector
    question_vector = text_to_fake_vector(question)

    # TODO 3：用 search(question_vector, documents) 得到 context 和 score
    context,score = search(question_vector,documents)
    if score == 0:
        print("没有检索到相关资料，停止调用模型。")
        print("模型回答：我没有在知识库中找到相关信息。")
        return
    
    # TODO 4：打印检索到的资料和分数，方便 debug
    print("检索到的资料：",context)
    print("分数：",score)
    # TODO 5：写 system_prompt
    # 要求模型只能根据资料回答，资料没有答案就拒答

    system_prompt = """
你是一个严格的知识库问答助手。
你只能根据提供的资料回答问题。
如果资料中没有答案，请回答：我没有在知识库中找到相关信息。
回答要简洁清楚。
"""
    # TODO 6：拼接 user_prompt
    # 内容包括：
    # 下面是知识库资料：
    # {context}
    # 用户问题：
    # {question}

    user_prompt = f"""
下面是知识库资料：

{context}

用户问题：
{question}
"""

    # TODO 7：调用 deepseek_client.chat()
    answer = deepseek_client.chat(
        user_message=user_prompt,
        system_message=system_prompt,
        temperature=0.2,
        max_tokens=800,
        show_model_name=True
    )

    # TODO 8：打印模型回答
    print("模型回答：")
    print(answer)


if __name__ == "__main__":
    main()