"""
Run:
python -m scripts.day14_test_persist_index
"""

from pathlib import Path
from pprint import pprint

from app.rag_service import RAGService


def print_file_status(index_path: Path, chunks_path: Path) -> None:
    print(f"faiss.index exists: {index_path.exists()}")
    print(f"chunks.json exists: {chunks_path.exists()}")


def create_service() -> RAGService:
    return RAGService(
        knowledge_base_dir="data/knowledge_base",
        chunk_size=120,
        chunk_overlap=30,
        top_k=3,
        similarity_threshold=0.65,
        persist_dir="data/vector_store",
    )


def main() -> None:
    persist_dir = Path("data/vector_store")
    index_path = persist_dir / "faiss.index"
    chunks_path = persist_dir / "chunks.json"

    print("Day 14 FAISS index persistence test")
    print("Current persisted index files:")
    print_file_status(index_path, chunks_path)

    try:
        print("\n[1] First RAGService initialization")
        service = create_service()
        print("Index files after first initialization:")
        print_file_status(index_path, chunks_path)
        print(f"chunk count: {len(service.chunks)}")

        if not index_path.exists():
            raise RuntimeError("faiss.index was not generated")
        if not chunks_path.exists():
            raise RuntimeError("chunks.json was not generated")

        print("\n[2] Second RAGService initialization")
        service2 = create_service()
        print(f"loaded chunk count: {len(service2.chunks)}")

        print("\n[3] Ask test")
        result = service2.ask("开发 Python 后端 API 接口服务推荐用什么框架？")
        print("answer:")
        print(result.get("answer", ""))
        print("retrieval_info:")
        pprint(result.get("retrieval_info", {}))
        print(f"sources count: {len(result.get('sources', []))}")

    except Exception as exc:
        print("\nDay 14 persistence test failed:")
        print(f"{type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    main()
