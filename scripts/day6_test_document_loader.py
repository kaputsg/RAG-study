"""
Day 6：测试 app.document_loader 模块
"""

from app.document_loader import DocumentLoader


def main():
    loader = DocumentLoader("data/knowledge_base")

    documents = loader.load_txt_documents()
    chunks = loader.load_and_split(chunk_size=120, chunk_overlap=30)

    print("读取到的文档数量：", len(documents))
    print("切分后的 chunk 数量：", len(chunks))

    print("\n前 5 个 chunk：")
    for chunk in chunks[:5]:
        print("来源：", chunk["source"])
        print("编号：", chunk["chunk_index"])
        print("内容：", chunk["text"])
        print("-" * 40)


if __name__ == "__main__":
    main()