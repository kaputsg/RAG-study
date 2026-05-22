from sentence_transformers import SentenceTransformer

from app.deepseek_client import deepseek_client

from scripts.day3_embedding_similarity import (
    MODEL_NAME,
    documents,
    cosine_similarity,
    search_top_k
)

SIMILARITY_THRESHOLD = 0.65

def main():
    """
    真实 Embedding 版最小 RAG Demo。

    流程：
    1. 定义用户问题
    2. 加载 BGE embedding 模型
    3. 把问题和文档转成向量
    4. 检索 top_k 相关文档
    5. 拼接 context
    6. 把 context + question 交给 DeepSeek
    """

    question = "数据库事务的 ACID 是什么？"

    # TODO 1：加载 embedding 模型
    model = SentenceTransformer(MODEL_NAME)

    # TODO 2：生成 question_embedding
    question_embedding = model.encode(question)
    # TODO 3：生成 document_embeddings
    document_embeddings = model.encode(documents)

    # TODO 4：调用 search_top_k，top_k=3
    top_results = search_top_k(
        question_embedding=question_embedding,
        document_embeddings=document_embeddings,
        documents_list=documents,
        top_k=3
    )

    best_score = top_results[0]["score"]

    if best_score < SIMILARITY_THRESHOLD:
        print("没有检索到足够相关的资料，停止调用模型。")
        print("模型回答：我没有在知识库中找到相关信息。")
        return

    # TODO 5：打印 top_k 检索结果
    for item in top_results:
        print("文档：", item["text"])
        print("相似度：", item["score"])
        print("-" * 30)

    print("\n用户问题：")
    print(question)
    # TODO 6：把 top_results 里的 text 拼成 context
    # 提示：
    # context = "\n\n".join([item["text"] for item in top_results])
    context = "\n\n".join([item["text"] for item in top_results])


    # TODO 7：写 system_prompt
    # 要求：只能根据资料回答，资料没有答案就拒答
    system_prompt = """
        你是一个严格的知识库问答助手。
        你只能根据提供的资料回答。
        如果资料中没有答案，请回答：我没有在知识库中找到相关信息。
        不要使用资料外的知识。
        回答要简洁清楚。
    """

    # TODO 8：写 user_prompt
    # 包含 context 和 question
    user_prompt = f"""
        下面是知识库资料：

        {context}

        用户问题：
        {question}
    """

    # TODO 9：调用 deepseek_client.chat()
    answer = deepseek_client.chat(
        user_message=user_prompt,
        system_message=system_prompt,
        temperature=0.2,
        max_tokens=800,
        show_model_name=True
    )

    # TODO 10：打印模型回答
    print("模型回答：")
    print(answer)


if __name__ == "__main__":
    main()