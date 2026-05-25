"""
文档加载与文本切分模块。

职责：
1. 从本地知识库目录读取 txt 文档
2. 把长文本切分成 chunks
3. 为每个 chunk 保留 source 和 chunk_index
"""

from pathlib import Path


class DocumentLoader:
    """
    文档加载器。

    用法：
    loader = DocumentLoader("data/knowledge_base")
    documents = loader.load_txt_documents()
    chunks = loader.load_and_split()
    """

    def __init__(self, knowledge_base_dir: str = "data/knowledge_base"):
        """
        初始化文档加载器。

        参数：
        knowledge_base_dir：知识库文件夹路径
        """

        # TODO 1：把 knowledge_base_dir 转成 Path 对象
        # 提示：self.knowledge_base_dir = Path(knowledge_base_dir)
        self.knowledge_base_dir = Path(knowledge_base_dir)

    def load_txt_documents(self):
        """
        读取知识库目录下所有 txt 文件。

        返回：
        [
            {
                "source": "文件路径",
                "text": "文件内容"
            }
        ]
        """

        documents = []

        # TODO 1：遍历 self.knowledge_base_dir 下所有 .txt 文件
        # 要求：使用 sorted() 保证顺序稳定

            # TODO 2：读取文本，encoding="utf-8"

            # TODO 3：构造 document 字典

            # TODO 4：append 到 documents

        for file_path in sorted(self.knowledge_base_dir.glob("*.txt")):

            text = file_path.read_text(encoding="utf-8")

            document = {
                "source": str(file_path),
                "text": text
            }

            documents.append(document)

        return documents

    def split_text(self, text: str, chunk_size: int = 120, chunk_overlap: int = 30):
        """
        把长文本切分成多个 chunk。

        参数：
        text：原始文本
        chunk_size：每个 chunk 的长度
        chunk_overlap：相邻 chunk 的重叠长度

        返回：
        ["chunk1", "chunk2", ...]
        """

        chunks = []

        # TODO 1：检查 chunk_overlap 必须小于 chunk_size

        # TODO 2：text.strip()

        # TODO 3：start = 0

        # TODO 4：while start < len(text):

            # TODO 5：end = start + chunk_size

            # TODO 6：chunk = text[start:end].strip()

            # TODO 7：如果 chunk 非空，append 到 chunks

            # TODO 8：如果 end >= len(text)，break

            # TODO 9：start = end - chunk_overlap

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

    def load_and_split(self, chunk_size: int = 120, chunk_overlap: int = 30):
        """
        读取所有 txt 文档，并切分成 chunks。

        返回：
        [
            {
                "source": "文件路径",
                "chunk_index": 0,
                "text": "chunk 内容"
            }
        ]
        """

        all_chunks = []

        # TODO 1：调用 self.load_txt_documents()

        # TODO 2：遍历 documents

            # TODO 3：取 source 和 text

            # TODO 4：调用 self.split_text()

            # TODO 5：遍历 chunks，构造 chunk_data

            # TODO 6：append 到 all_chunks

        documents = self.load_txt_documents()

        for document in documents:
            source = document["source"]
            text = document["text"]

            chunks = self.split_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

            for index, chunk in enumerate(chunks):
                chunk_data = {
                    "source": source,
                    "chunk_index": index,
                    "text": chunk
                }

                all_chunks.append(chunk_data)

        return all_chunks