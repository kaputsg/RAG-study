"""
Day 5：文档加载与文本切分

目标：
1. 从 data/knowledge_base 读取 txt 文件
2. 把每个文件内容加载成 document
3. 把长文本切成多个 chunk
4. 每个 chunk 保留来源 source
"""

from pathlib import Path


KNOWLEDGE_BASE_DIR = Path("data/knowledge_base")


def load_txt_documents(folder_path):
    """
    读取指定文件夹下的所有 .txt 文件。

    返回格式：
    [
        {
            "source": "文件路径",
            "text": "文件内容"
        }
    ]
    """

    documents = []

    # TODO 1：遍历 folder_path 下所有 .txt 文件
    # 提示：folder_path.glob("*.txt")
    
        # TODO 2：读取文件内容
        # 提示：file_path.read_text(encoding="utf-8")

        # TODO 3：构造 document 字典
        # {
        #     "source": str(file_path),
        #     "text": text
        # }

        # TODO 4：append 到 documents
    for file_path in sorted(folder_path.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")
        document = {
            "source": str(file_path),
            "text": text
        }
        documents.append(document)

    

    return documents


def split_text(text, chunk_size=120, chunk_overlap=30):
    """
    把长文本切成多个 chunk。

    参数：
    text：原始长文本
    chunk_size：每块长度
    chunk_overlap：相邻块重叠长度

    返回：
    ["chunk1", "chunk2", ...]
    """

    chunks = []

    # TODO 1：准备 start = 0

    # TODO 2：while start < len(text):

        # TODO 3：end = start + chunk_size

        # TODO 4：chunk = text[start:end]

        # TODO 5：把 chunk 加入 chunks

        # TODO 6：更新 start
        # 提示：start = end - chunk_overlap
    start = 0

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap 必须小于 chunk_size")

    text = text.strip()
    
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def main():
    documents = load_txt_documents(KNOWLEDGE_BASE_DIR)

    print("读取到的文档数量：", len(documents))

    all_chunks = []

    for document in documents:
        source = document["source"]
        text = document["text"]

        chunks = split_text(text, chunk_size=120, chunk_overlap=30)

        for index, chunk in enumerate(chunks):
            chunk_data = {
                "source": source,
                "chunk_index": index,
                "text": chunk
            }

            all_chunks.append(chunk_data)

    print("切分后的 chunk 数量：", len(all_chunks))

    print("\n前 5 个 chunk：")
    for chunk in all_chunks[:5]:
        print("来源：", chunk["source"])
        print("编号：", chunk["chunk_index"])
        print("内容：", chunk["text"])
        print("-" * 40)


if __name__ == "__main__":
    main()