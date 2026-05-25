"""
Day 6：测试 app.rag_service 模块
"""

from app.rag_service import RAGService


def main():
    rag_service = RAGService(
        knowledge_base_dir="data/knowledge_base",
        chunk_size=120,
        chunk_overlap=30,
        top_k=3,
        similarity_threshold=0.65
    )

    question = "开发 Python 后端 API 接口服务推荐用什么框架？"

    result = rag_service.ask(question)

    print("用户问题：")
    print(question)

    print("\n模型回答：")
    print(result["answer"])

    print("\n引用来源：")
    for source in result["sources"]:
        print("来源：", source["source"])
        print("片段编号：", source["chunk_index"])
        print("分数：", source["score"])
        print("内容：", source["text"])
        print("-" * 40)


if __name__ == "__main__":
    main()