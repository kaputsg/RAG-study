from app.deepseek_client import deepseek_client

from scripts.day4_faiss_bge import (
    documents,
    search_with_faiss
)


SIMILARITY_THRESHOLD = 0.65


def main():
    question = "数据库事务的 ACID 是什么？"
    # TODO 1：调用 search_with_faiss，拿到 top_results
    top_results = search_with_faiss(question, documents, top_k=3)

    # TODO 2：打印 top_results，观察文档和分数
    print("Top Results:")
    for item in top_results:
        print(f"Score: {item['score']:.4f}, Text: {item['text']}")

    # TODO 3：取出最高分 best_score
    best_score = max(item['score'] for item in top_results)

    # TODO 4：如果 best_score < SIMILARITY_THRESHOLD，直接拒答并 return
    if best_score < SIMILARITY_THRESHOLD:
        print("没有检索到足够相关的资料，停止调用模型。")
        print("模型回答：我没有在知识库中找到相关信息。")
        return

    # TODO 5：把 top_results 里的 text 拼接成 context
    # 提示：context = "\n\n".join([item["text"] for item in top_results])
    context = "\n\n".join(item["text"] for item in top_results)

    # TODO 6：写 system_prompt
    # 要求：只能根据资料回答；资料没有答案就拒答；回答简洁
    system_prompt = """
    你是一个严格的知识库问答助手。
    你只能根据用户提供的资料回答问题。
    如果资料中没有相关信息，请回答：我没有在知识库中找到相关信息。
    回答要简洁清楚，不要添加资料外的信息。
    """

    # TODO 7：写 user_prompt，把 context 和 question 放进去
    user_prompt = f"""
    下面是知识库资料：

    {context}

    用户问题：
    {question}
    """

    # TODO 8：调用 deepseek_client.chat()
    response = deepseek_client.chat(
        user_message=user_prompt,
        system_message=system_prompt,
        temperature=0.2,
        max_tokens=800,
        show_model_name=True
    )

    # TODO 9：打印模型回答
    print("\n模型回答：")
    print(response)

if __name__ == "__main__":
    main()