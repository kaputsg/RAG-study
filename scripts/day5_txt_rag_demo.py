"""
Day 5：本地 txt 知识库 RAG Demo

目标：
1. 读取 data/knowledge_base 下的 txt 文档
2. 切分成 chunks
3. 使用 BGE + FAISS 检索相关 chunks
4. 把 chunks 拼成 context
5. 调用 DeepSeek 根据资料回答
"""

from app.deepseek_client import deepseek_client

from scripts.day5_document_loader import (
    KNOWLEDGE_BASE_DIR,
    load_txt_documents
)

from scripts.day5_chunk_faiss_search import (
    build_chunks,
    search_chunks_with_faiss
)


def build_context(search_results):
    """
    把检索结果拼成 context。

    每个 chunk 保留来源和编号，方便模型知道资料来源。
    """

    context_parts = []

    # TODO 1：遍历 search_results

        # TODO 2：取出 source、chunk_index、text、score

        # TODO 3：拼成一段带来源的信息

        # TODO 4：append 到 context_parts

    # TODO 5：用 "\n\n".join(context_parts) 拼成 context
    for i in search_results:
        source = i["source"]
        chunk_index = i["chunk_index"]
        text = i["text"]
        score = i["score"]

        context_part = f"""
        [来源: {source} | 片段: {chunk_index} | 分数: {score:.4f}]
        {text}
        """
        context_parts.append(context_part)

    return "\n\n".join(context_parts)


def main():
    question = "数据库事务的 ACID 是什么？"

    # TODO 1：读取 txt 文档

    # TODO 2：构建 chunks

    # TODO 3：调用 search_chunks_with_faiss() 检索 top_k=3

    # TODO 4：打印检索结果，方便 debug

    # TODO 5：如果 search_results 为空，直接拒答并 return

    # TODO 6：调用 build_context(search_results)，得到 context

    # TODO 7：写 system_message
    # 要求：
    # - 只能根据资料回答
    # - 资料没有答案就拒答
    # - 回答简洁
    # - 不要使用资料外知识

    # TODO 8：写 user_message
    # 包含 context 和 question

    # TODO 9：调用 deepseek_client.chat()
    # 注意参数名是 user_message 和 system_message，不是 user_prompt/system_prompt

    # TODO 10：打印模型回答
    documents = load_txt_documents(KNOWLEDGE_BASE_DIR)
    chunks = build_chunks(documents, chunk_size=120, chunk_overlap=30)
    search_results = search_chunks_with_faiss(
        question=question,
        chunks=chunks,
        top_k=3
    )

    if not search_results:
        print("没有检索到足够相关的资料，停止调用模型。")
        print("模型回答：我没有在知识库中找到相关信息。")
        return
    
    context = build_context(search_results)

    system_message = """
    你是一个严格的知识库问答助手。
    你只能根据用户提供的知识库资料回答问题。
    如果资料中没有相关信息，请回答：我没有在知识库中找到相关信息。
    不要使用资料外的知识。
    回答要简洁清楚。
    """

    user_message = f"""
    下面是知识库资料：

    {context}

    用户问题：
    {question}
    """

    answer = deepseek_client.chat(
        user_message=user_message,
        system_message=system_message,
        temperature=0.2,
        max_tokens=800,
        show_model_name=True
    )

    print("模型回答：")
    print(answer)

if __name__ == "__main__":
    main()