"""
向量库模块。

职责：
1. 使用 BGE 模型把 chunks 转成 embedding
2. 使用 FAISS 建立本地向量索引
3. 根据用户问题检索相关 chunks
"""

import json
from pathlib import Path

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class VectorStore:
    """
    本地向量库。

    用法：
    vector_store = VectorStore()
    vector_store.build_index(chunks)
    results = vector_store.search("用户问题", top_k=3)
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-zh-v1.5",
        similarity_threshold: float = 0.65
    ):
        """
        初始化向量库。

        参数：
        model_name：embedding 模型名称
        similarity_threshold：相似度阈值，低于该分数的结果会被过滤
        """

        # TODO 1：保存 model_name

        # TODO 2：保存 similarity_threshold

        # TODO 3：加载 SentenceTransformer 模型

        # TODO 4：初始化 self.index = None

        # TODO 5：初始化 self.chunks = []

        self.model_name = model_name
        self.similarity_threshold = similarity_threshold
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, chunks):
        """
        根据 chunks 建立 FAISS 索引。

        参数：
        chunks：
        [
            {
                "source": "...",
                "chunk_index": 0,
                "text": "chunk 内容"
            }
        ]
        """

        # TODO 1：保存 chunks 到 self.chunks

        # TODO 2：从 chunks 中取出所有 text
        # 提示：texts = [chunk["text"] for chunk in chunks]

        # TODO 3：如果 texts 为空，抛出 ValueError

        # TODO 4：使用 self.model.encode(texts) 生成 embeddings

        # TODO 5：转成 np.float32 数组

        # TODO 6：faiss.normalize_L2(vectors)

        # TODO 7：获取 dimension

        # TODO 8：创建 faiss.IndexFlatIP(dimension)

        # TODO 9：把 vectors 加入 self.index
        self.chunks = chunks
        texts = [chunk["text"] for chunk in chunks]
        
        if not texts:
            raise ValueError("没有文本可供建立索引")
        
        embeddings = self.model.encode(texts)
        
        vectors = np.array(embeddings).astype("float32")
        
        faiss.normalize_L2(vectors)
        
        dimension = vectors.shape[1]
        
        self.index = faiss.IndexFlatIP(dimension)
        
        self.index.add(vectors)

    def save(self, index_path: str | Path, chunks_path: str | Path) -> None:
        """
        保存 FAISS 索引和 chunks 元数据到本地文件。
        """

        if self.index is None:
            raise ValueError("没有可保存的 FAISS 索引，请先调用 build_index")

        index_path = Path(index_path)
        chunks_path = Path(chunks_path)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        chunks_path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(index_path))

        with chunks_path.open("w", encoding="utf-8") as file:
            json.dump(self.chunks, file, ensure_ascii=False, indent=2)

    def load(self, index_path: str | Path, chunks_path: str | Path) -> None:
        """
        从本地文件加载 FAISS 索引和 chunks 元数据。
        """

        index_path = Path(index_path)
        chunks_path = Path(chunks_path)

        if not index_path.exists():
            raise FileNotFoundError(f"FAISS 索引文件不存在: {index_path}")
        if not chunks_path.exists():
            raise FileNotFoundError(f"chunks 元数据文件不存在: {chunks_path}")

        self.index = faiss.read_index(str(index_path))

        with chunks_path.open("r", encoding="utf-8") as file:
            self.chunks = json.load(file)

    def has_persisted_index(
        self,
        index_path: str | Path,
        chunks_path: str | Path
    ) -> bool:
        """
        检查本地 FAISS 索引和 chunks 元数据是否同时存在。
        """

        return Path(index_path).exists() and Path(chunks_path).exists()

    def search(self, question: str, top_k: int = 3):
        """
        检索和用户问题最相关的 chunks。

        返回：
        [
            {
                "source": "...",
                "chunk_index": 0,
                "text": "...",
                "score": 0.75
            }
        ]
        """

        results = []

        # TODO 1：如果 self.index is None，抛出 ValueError
        # 提示：必须先 build_index，再 search

        # TODO 2：把 question 转成 embedding

        # TODO 3：转成二维 np.float32 数组
        # 提示：query_vector = np.array([question_embedding]).astype("float32")

        # TODO 4：faiss.normalize_L2(query_vector)

        # TODO 5：调用 self.index.search(query_vector, top_k)

        # TODO 6：遍历 indices[0] 和 scores[0]

            # TODO 7：如果 score < self.similarity_threshold，continue

            # TODO 8：根据 global_chunk_index 找到 chunk
            # 提示：chunk = self.chunks[global_chunk_index]

            # TODO 9：组装 result，append 到 results

        if self.index is None:
            raise ValueError("必须先 build_index，再 search")
        
        question_embedding = self.model.encode(question)
        query_vector = np.array([question_embedding]).astype("float32")
        faiss.normalize_L2(query_vector)
        scores, indices = self.index.search(query_vector, top_k)

        for score, global_chunk_index in zip(scores[0], indices[0]):

            if score < self.similarity_threshold:
                continue

            chunk = self.chunks[global_chunk_index]

            result = {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "score": float(score)
            }

            results.append(result)

        return results
