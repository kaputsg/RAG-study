"""
Day 4：FAISS 基础练习

目标：
1. 准备几段文档
2. 准备对应的假向量
3. 把向量存入 FAISS
4. 用问题向量搜索 top_k
5. 根据 FAISS 返回的编号找回原文
"""

import numpy as np
import faiss


documents = [
    "Python 可以用于 Web 后端开发、自动化脚本、数据分析和人工智能应用。",
    "FastAPI 是一个高性能 Python Web 框架，适合开发 API 接口服务。",
    "RAG 是检索增强生成技术，它会先检索知识库资料，再让大模型生成答案。",
    "Vue 是一个前端框架，可以用来构建用户界面。",
    "今天晚上吃什么比较好，可以根据自己的口味选择。"
]


# 每个向量对应一段文档
# 维度顺序：Python、后端、接口、前端、RAG、生活
document_vectors = [
    [1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1],
]


question = "后端服务一般用什么工具开发？"

# 问题向量：后端 + 接口
question_vector = [0, 1, 1, 0, 0, 0]


def main():
    # TODO 1：把 document_vectors 转成 numpy 数组
    # 要求 dtype 是 float32
    # 提示：np.array(document_vectors).astype("float32")
    vectors = np.array(document_vectors).astype("float32")
    # TODO 2：获取向量维度
    # 提示：dimension = vectors.shape[1]
    dimension = vectors.shape[1]

    # TODO 3：创建 FAISS 索引
    # 先用 IndexFlatIP，IP 表示 inner product，内积
    # 提示：index = faiss.IndexFlatIP(dimension)
    index = faiss.IndexFlatIP(dimension)

    # TODO 4：把文档向量加入 index
    # 提示：index.add(vectors)
    index.add(vectors)

    # TODO 5：把 question_vector 转成二维 numpy 数组
    # 注意 FAISS 需要二维数组，形状类似 (1, 6)
    # 提示：np.array([question_vector]).astype("float32")
    query_vector = np.array([question_vector]).astype("float32")

    # TODO 6：搜索 top_k=3
    # 提示：scores, indices = index.search(query_vector, 3)
    scores, indices = index.search(query_vector, 3)

    # TODO 7：打印 scores 和 indices，先看 FAISS 返回什么
    print("Scores:", scores)
    print("Indices:", indices)
    # TODO 8：根据 indices 找回原文
    # 提示：indices[0] 是第一条 query 的 top_k 结果编号
    # for doc_index in indices[0]:
    #     print(documents[doc_index])
    for doc_index in indices[0]:
        print(documents[doc_index])


if __name__ == "__main__":
    main()