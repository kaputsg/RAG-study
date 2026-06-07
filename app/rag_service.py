"""
RAG 服务模块。

职责：
1. 加载本地知识库文档
2. 建立向量索引
3. 根据用户问题检索相关 chunks
4. 拼接 context
5. 调用 DeepSeek 生成答案
"""

from pathlib import Path

from app.document_loader import DocumentLoader
from app.vector_store import VectorStore
from app.deepseek_client import deepseek_client
from app.index_manifest import (
    build_manifest,
    has_manifest,
    load_manifest,
    manifest_matches,
    save_manifest,
)


class RAGService:
    """
    RAG 问答服务。

    用法：
    rag_service = RAGService()
    answer = rag_service.ask("用户问题")
    """

    def __init__(
        self,
        knowledge_base_dir: str = "data/knowledge_base",
        chunk_size: int = 120,
        chunk_overlap: int = 30,
        top_k: int = 3,
        similarity_threshold: float = 0.65,
        persist_dir: str = "data/vector_store"
    ):
        """
        初始化 RAG 服务。

        参数：
        knowledge_base_dir：知识库目录
        chunk_size：chunk 大小
        chunk_overlap：chunk 重叠长度
        top_k：检索返回数量
        similarity_threshold：相似度阈值
        """

        # TODO 1：保存参数到 self

        # TODO 2：创建 DocumentLoader

        # TODO 3：创建 VectorStore

        # TODO 4：初始化 self.chunks = []

        # TODO 5：调用 self.build_knowledge_base()

        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.persist_dir = Path(persist_dir)
        self.index_path = self.persist_dir / "faiss.index"
        self.chunks_path = self.persist_dir / "chunks.json"
        self.manifest_path = self.persist_dir / "manifest.json"

        self.document_loader = DocumentLoader(self.knowledge_base_dir)
        self.vector_store = VectorStore(similarity_threshold=self.similarity_threshold)
        self.chunks = []

        self.load_or_build_knowledge_base()

    def load_or_build_knowledge_base(self):
        """
        优先加载本地持久化索引；如果不存在，则重新构建知识库索引。
        """

        current_manifest = build_manifest(self.knowledge_base_dir)
        has_index = self.vector_store.has_persisted_index(
            self.index_path,
            self.chunks_path
        )
        has_saved_manifest = has_manifest(self.manifest_path)

        if not has_index:
            print("未发现本地索引，开始重新构建知识库索引...")
            self.build_knowledge_base()
            return

        if not has_saved_manifest:
            print("未发现 manifest，开始重新构建知识库索引...")
            self.build_knowledge_base()
            return

        try:
            saved_manifest = load_manifest(self.manifest_path)
        except Exception as error:
            print(f"manifest 读取失败，开始重新构建知识库索引：{error}")
            self.build_knowledge_base()
            return

        if manifest_matches(current_manifest, saved_manifest):
            self.vector_store.load(self.index_path, self.chunks_path)
            self.chunks = self.vector_store.chunks
            print(f"已加载本地向量索引，知识库未变化，chunk 数量：{len(self.chunks)}")
            return

        print("知识库文件已变化，开始重新构建知识库索引...")
        self.build_knowledge_base()

    def build_knowledge_base(self):
        """
        加载文档、切分 chunks，并建立向量索引。
        """

        # TODO 1：使用 self.document_loader.load_and_split()

        # TODO 2：保存到 self.chunks

        # TODO 3：如果 chunks 为空，抛出 ValueError

        # TODO 4：调用 self.vector_store.build_index(self.chunks)

        print("开始构建新的知识库索引...")
        self.chunks = self.document_loader.load_and_split(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        if not self.chunks:
            raise ValueError("没有加载到任何文档，请检查知识库目录。")
        
        self.vector_store.build_index(self.chunks)
        self.vector_store.save(self.index_path, self.chunks_path)
        print(f"向量索引保存成功：{self.index_path}，chunks：{self.chunks_path}")
        current_manifest = build_manifest(self.knowledge_base_dir)
        save_manifest(current_manifest, self.manifest_path)
        print("manifest 已更新")


    def build_context(self, search_results):
        """
        把检索结果拼成 context。
        """

        context_parts = []

        # TODO 1：遍历 search_results

            # TODO 2：取出 source、chunk_index、score、text

            # TODO 3：拼成带来源的片段

            # TODO 4：append 到 context_parts

        # TODO 5：return "\n\n".join(context_parts)

        for result in search_results:

            source = result.get("source", "未知来源")
            chunk_index = result.get("chunk_index", -1)
            score = result.get("score", 0)
            text = result.get("text", "")
            context_part = f"来源: {source} (chunk {chunk_index}, 相似度 {score:.2f})\n{text}"
            context_parts.append(context_part)

        return "\n\n".join(context_parts)

    def ask(self, question: str):
        """
        根据用户问题进行 RAG 问答。

        返回：
        {
            "answer": "模型回答",
            "sources": 检索结果
        }
        """

        # TODO 1：调用 self.vector_store.search(question, self.top_k)

        # TODO 2：如果没有 search_results，直接返回拒答结果

        # TODO 3：构建 context

        # TODO 4：写 system_message

        # TODO 5：写 user_message

        # TODO 6：调用 deepseek_client.chat()

        # TODO 7：返回 {"answer": answer, "sources": search_results}

        search_results = self.vector_store.search(question, self.top_k)
        max_score = max(
            (result.get("score", 0) for result in search_results),
            default=0
        )

        if max_score >= 0.75:
            confidence = "high"
        elif max_score >= 0.65:
            confidence = "medium"
        else:
            confidence = "low"

        retrieval_info = {
            "hit": bool(search_results),
            "max_score": max_score,
            "source_count": len(search_results),
            "confidence": confidence
        }

        if not search_results:
            return {
                "answer": "我没有在知识库中找到相关信息。",
                "sources": [],
                "retrieval_info": retrieval_info
            }
        
        context = self.build_context(search_results)

        system_message = """
        你是一个知识丰富的助手，
        基于以下提供的上下文信息来回答用户的问题。
        请尽量详细地回答，并且只使用提供的上下文信息，
        不要凭空编造。"""

        user_message = f"""
        下面是知识库资料：

        {context}

        用户问题：
        {question}
        """

        answer = deepseek_client.chat(
            user_message=user_message,
            system_message=system_message,
            temperature=0.2,
            max_tokens=800,
            show_model_name=True
        )

        return {
            "answer": answer,
            "sources": search_results,
            "retrieval_info": retrieval_info
        }
