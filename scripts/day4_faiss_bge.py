"""
Day 4：FAISS + BGE 真实向量检索

目标：
1. 使用 BGE 模型生成真实文档向量
2. 把文档向量加入 FAISS
3. 使用问题向量检索 top_k 文档
4. 根据 FAISS 返回的 indices 找回原文
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-zh-v1.5"


documents = [
    "Python 可以用于 Web 后端开发、自动化脚本、数据分析和人工智能应用。",
    "FastAPI 是一个高性能 Python Web 框架，适合开发 API 接口服务。",
    "RAG 是检索增强生成技术，它会先检索知识库资料，再让大模型生成答案。",
    "Vue 是一个前端框架，可以用来构建用户界面。",
    "今天晚上吃什么比较好，可以根据自己的口味选择。"
]


question = "开发 Python 后端 API 接口服务用什么框架？"

def search_with_faiss(question, documents, top_k=3):
    """
    使用 BGE + FAISS 检索最相关的 top_k 文档。

    参数：
    question：用户问题
    documents：文档文本列表
    top_k：返回前几个结果

    返回：
    [
        {"text": 文档内容, "score": 相似度分数},
        ...
    ]
    """

    results = []

    # TODO 1：加载 BGE 模型
    model = SentenceTransformer(MODEL_NAME)

    # TODO 2：把 documents 转成 embeddings
    document_embeddings = model.encode(documents)

    # TODO 3：转成 float32 numpy 数组
    vectors = np.array(document_embeddings).astype("float32")

    # TODO 4：归一化文档向量
    faiss.normalize_L2(vectors)

    # TODO 5：创建 FAISS index
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # TODO 6：把文档向量加入 index
    index.add(vectors)

    # TODO 7：把 question 转成 embedding
    question_embedding = model.encode(question)

    # TODO 8：转成二维 float32 query_vector
    query_vector = np.array([question_embedding]).astype("float32")

    # TODO 9：归一化 query_vector
    faiss.normalize_L2(query_vector)

    # TODO 10：用 index.search(query_vector, top_k) 搜索
    scores, indices = index.search(query_vector, top_k)

    # TODO 11：根据 indices 和 scores 组装 results
    for rank, doc_index in enumerate(indices[0]):
        results.append({
            "text": documents[doc_index],
            "score": float(scores[0][rank])
        })

    return results


def main():
    results = search_with_faiss(
        question=question,
        documents=documents,
        top_k=3
    )

    print("用户问题：")
    print(question)

    print("\nTop 3 检索结果：")
    for item in results:
        print("文档：", item["text"])
        print("分数：", item["score"])
        print("-" * 30)


if __name__ == "__main__":
    main()