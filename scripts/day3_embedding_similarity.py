"""
Day 3：真实 Embedding 相似度检索

目标：
1. 加载 BGE 中文 embedding 模型
2. 把用户问题和多段文档转成真实向量
3. 手写余弦相似度
4. 找出最相关文档
"""

import numpy as np
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


def cosine_similarity(vector1, vector2):
    """
    计算两个向量的余弦相似度。

    公式：
    dot(vector1, vector2) / (norm(vector1) * norm(vector2))

    TODO：
    1. 计算 dot_product
    2. 计算 vector1_norm
    3. 计算 vector2_norm
    4. 返回 dot_product / (vector1_norm * vector2_norm)
    """

    # TODO：你自己写
    dot_product = np.dot(vector1,vector2)
    v1 = np.array(vector1)
    vector1_norm = np.linalg.norm(v1)
    v2 = np.array(vector2)
    vector2_norm = np.linalg.norm(v2)

    cos = dot_product / (vector1_norm * vector2_norm)
    return cos



def search(question_embedding, document_embeddings, documents_list):
    """
    找出和用户问题最相似的文档。

    TODO：
    1. 准备 best_document = None
    2. 准备 best_score = -1
    3. 遍历 documents_list
    4. 取出对应 document_embedding
    5. 调用 cosine_similarity()
    6. 打印每段文档的相似度
    7. 更新最高分文档
    8. 返回 best_document 和 best_score
    """

    # TODO：你自己写

    best_document = None
    best_score = -1
    for i in range(len(documents_list)):
        document = documents_list[i]
        document_embedding = document_embeddings[i]
        score = cosine_similarity(question_embedding,document_embedding)
        print("当前文档：", document)
        print("文档相似度：", score)
        print("-" * 30)
        if score > best_score:
            best_score = score
            best_document = document

    return best_document,best_score

def search_top_k(question_embedding, document_embeddings, documents_list, top_k=3):
    """
    返回相似度最高的 top_k 个文档。

    目标：
    1. 遍历所有文档
    2. 计算每个文档和问题的相似度
    3. 把 {"text": document, "score": score} 放进 results
    4. 按 score 从高到低排序
    5. 返回前 top_k 个结果
    """

    results = []

    # TODO 1：遍历 documents_list
    # 提示：for i in range(len(documents_list)):

        # TODO 2：取出 document 和 document_embedding

        # TODO 3：计算 score

        # TODO 4：把结果 append 到 results
        # 格式建议：
        # {
        #     "text": document,
        #     "score": score
        # }

    # TODO 5：按 score 从高到低排序
    # 提示：
    # results.sort(key=lambda item: item["score"], reverse=True)

    # TODO 6：返回前 top_k 个
    # 提示：
    # return results[:top_k]
    for i in range(len(documents_list)):
        document = documents_list[i]
        document_embedding = document_embeddings[i]
        score = cosine_similarity(question_embedding,document_embedding)
        results.append({
            "text": document,
            "score": score
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]



def main():
    # TODO 1：加载模型
    model = SentenceTransformer(MODEL_NAME)
    # TODO 2：把 question 转成向量
    question_embedding = model.encode(question)

    # TODO 3：把 documents 转成向量
    document_embeddings = model.encode(documents)

    # TODO 4：调用 search()
    #result, score = search(question_embedding, document_embeddings, documents)

    top_results = search_top_k(
        question_embedding=question_embedding,
        document_embeddings=document_embeddings,
        documents_list=documents,
        top_k=3
    )
    
    print("\nTop 3 检索结果：")
    for item in top_results:
        print("文档：", item["text"])
        print("相似度：", item["score"])
        print("-" * 30)


    print("\n用户问题：")
    print(question)

    #print("\n最相关资料：")
    #print(result)

    #print("\n相似度分数：")
    #print(score)


if __name__ == "__main__":
    main()