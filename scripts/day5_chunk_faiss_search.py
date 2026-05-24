"""
Day 5：真实文档 Chunk + FAISS 检索

目标：
1. 从 data/knowledge_base 读取 txt 文件
2. 把文档切成 chunks
3. 对 chunks 做 BGE embedding
4. 存入 FAISS
5. 根据用户问题检索最相关 chunks
6. 打印来源 source 和 chunk_index
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from scripts.day5_document_loader import (
    KNOWLEDGE_BASE_DIR,
    load_txt_documents,
    split_text
)


MODEL_NAME = "BAAI/bge-small-zh-v1.5"

SIMILARITY_THRESHOLD = 0.65


def build_chunks(documents, chunk_size=120, chunk_overlap=30):
    """
    把 documents 转换成 chunks。

    输入 documents：
    [
        {"source": "...", "text": "..."}
    ]

    输出 chunks：
    [
        {
            "source": "文件路径",
            "chunk_index": 0,
            "text": "chunk 内容"
        }
    ]
    """

    all_chunks = []

    # TODO 1：遍历 documents

        # TODO 2：取出 source 和 text

        # TODO 3：调用 split_text(text, chunk_size, chunk_overlap)

        # TODO 4：遍历 chunks，构造 chunk_data

        # TODO 5：append 到 all_chunks

    for document in documents:
        source = document["source"]
        text = document["text"]

        text_chunks = split_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        for index, chunk in enumerate(text_chunks):
            chunk_data = {
                "source": source,
                "chunk_index": index,
                "text": chunk
            }
            all_chunks.append(chunk_data)

    return all_chunks


def search_chunks_with_faiss(question, chunks, top_k=3):
    """
    用 BGE + FAISS 检索最相关 chunks。

    返回：
    [
        {
            "source": "...",
            "chunk_index": 0,
            "text": "...",
            "score": 0.72
        }
    ]
    """

    results = []

    # TODO 1：加载 BGE 模型

    # TODO 2：从 chunks 中取出所有 chunk_texts
    # 提示：chunk_texts = [chunk["text"] for chunk in chunks]

    # TODO 3：把 chunk_texts 转成 embeddings

    # TODO 4：转成 float32 numpy 数组

    # TODO 5：归一化 vectors

    # TODO 6：创建 FAISS IndexFlatIP

    # TODO 7：把 vectors 加入 index

    # TODO 8：把 question 转成 embedding

    # TODO 9：转成二维 float32 query_vector

    # TODO 10：归一化 query_vector

    # TODO 11：搜索 top_k

    # TODO 12：根据 indices 找回 chunk，并组装 results
    # 注意：score 要转成 float
    model = SentenceTransformer(MODEL_NAME)

    chunk_texts = [chunk["text"] for chunk in chunks]

    chunk_embeddings = model.encode(chunk_texts)

    vectors = np.array(chunk_embeddings).astype("float32")

    faiss.normalize_L2(vectors)

    dimension = chunk_embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(vectors)

    question_embedding = model.encode([question], convert_to_numpy=True).astype("float32")

    faiss.normalize_L2(question_embedding)

    query_vector = question_embedding.reshape(1, -1)

    scores, indices = index.search(query_vector, top_k)

    for rank, global_chunk_index in enumerate(indices[0]):
        chunk = chunks[global_chunk_index]
        score = float(scores[0][rank])

        if score < SIMILARITY_THRESHOLD:
            continue

        results.append({
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
            "score": score
        })


    return results


def main():
    question = "开发 Python 后端 API 接口服务推荐用什么框架？"

    # TODO 1：读取 txt 文档

    # TODO 2：构建 chunks

    # TODO 3：打印文档数量和 chunk 数量

    # TODO 4：调用 search_chunks_with_faiss()

    # TODO 5：打印 Top K 检索结果
    # 要打印 source、chunk_index、score、text
    documents = load_txt_documents(KNOWLEDGE_BASE_DIR)
    chunks = build_chunks(documents, chunk_size=120, chunk_overlap=30)
    print(f"文档数量: {len(documents)}")
    print(f"Chunk 数量: {len(chunks)}")

    results = search_chunks_with_faiss(question, chunks, top_k=3)

    print("\nTop K 检索结果:")
    for result in results:
        print(f"Source: {result['source']}")
        print(f"Chunk Index: {result['chunk_index']}")
        print(f"Score: {result['score']}")
        print(f"Text: {result['text']}")
        print("-" * 50)


if __name__ == "__main__":
    main()