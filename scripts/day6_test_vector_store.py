"""
Day 6：测试 app.vector_store 模块
"""

from app.document_loader import DocumentLoader
from app.vector_store import VectorStore


def main():
    question = "开发 Python 后端 API 接口服务推荐用什么框架？"

    loader = DocumentLoader("data/knowledge_base")
    chunks = loader.load_and_split(chunk_size=120, chunk_overlap=30)

    print("chunk 数量：", len(chunks))

    vector_store = VectorStore(similarity_threshold=0.65)
    vector_store.build_index(chunks)

    results = vector_store.search(question, top_k=3)

    print("\n用户问题：")
    print(question)

    print("\nTop 检索结果：")
    for item in results:
        print("来源：", item["source"])
        print("片段编号：", item["chunk_index"])
        print("分数：", item["score"])
        print("内容：", item["text"])
        print("-" * 40)


if __name__ == "__main__":
    main()