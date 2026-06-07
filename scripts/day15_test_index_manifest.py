"""
Day 15 manifest mechanism test.

Run:
python -m scripts.day15_test_index_manifest
"""

from pathlib import Path
import json
import time

from app.rag_service import RAGService


def create_service() -> RAGService:
    return RAGService(
        knowledge_base_dir="data/knowledge_base",
        chunk_size=120,
        chunk_overlap=30,
        top_k=3,
        similarity_threshold=0.65,
        persist_dir="data/vector_store",
    )


def print_runtime_files(index_path: Path, chunks_path: Path, manifest_path: Path) -> None:
    print(f"faiss.index exists: {index_path.exists()}")
    print(f"chunks.json exists: {chunks_path.exists()}")
    print(f"manifest.json exists: {manifest_path.exists()}")


def remove_runtime_files(index_path: Path, chunks_path: Path, manifest_path: Path) -> None:
    for path in (index_path, chunks_path, manifest_path):
        if path.exists():
            path.unlink()


def main() -> None:
    knowledge_base_dir = Path("data/knowledge_base")
    persist_dir = Path("data/vector_store")
    index_path = persist_dir / "faiss.index"
    chunks_path = persist_dir / "chunks.json"
    manifest_path = persist_dir / "manifest.json"
    temp_file = knowledge_base_dir / "day15_manifest_temp.txt"

    service3: RAGService | None = None

    try:
        if temp_file.exists():
            temp_file.unlink()

        print("\n=== 1. 第一次初始化：生成索引和 manifest ===")
        remove_runtime_files(index_path, chunks_path, manifest_path)

        service1 = create_service()
        print_runtime_files(index_path, chunks_path, manifest_path)
        print(f"chunk count: {len(service1.chunks)}")

        if not index_path.exists():
            raise AssertionError("faiss.index was not created")
        if not chunks_path.exists():
            raise AssertionError("chunks.json was not created")
        if not manifest_path.exists():
            raise AssertionError("manifest.json was not created")

        with manifest_path.open("r", encoding="utf-8") as file:
            manifest = json.load(file)
        print(f"manifest file count: {len(manifest.get('files', []))}")

        print("\n=== 2. 第二次初始化：加载已有索引 ===")
        service2 = create_service()
        result2 = service2.ask("开发 Python 后端 API 接口服务推荐用什么框架？")
        print(f"answer preview: {result2['answer'][:100]}")
        print(f"retrieval_info: {result2['retrieval_info']}")
        print(f"sources count: {len(result2['sources'])}")

        print("\n=== 3. 修改知识库：检测变化并重建 ===")
        temp_file.write_text(
            "Day 15 manifest 测试文档。\n"
            "这个文件用于测试知识库文件变化后是否会触发索引重建。\n"
            "如果用户问 Day 15 manifest 测试，系统应该能检索到这个临时文档。\n",
            encoding="utf-8",
        )
        time.sleep(0.1)

        service3 = create_service()
        result3 = service3.ask("Day 15 manifest 测试文档是做什么的？")
        print(f"answer: {result3['answer']}")
        print(f"retrieval_info: {result3['retrieval_info']}")
        print(f"sources count: {len(result3['sources'])}")

        found_temp_source = any(
            Path(source.get("source", "")).name == temp_file.name
            for source in result3["sources"]
        )
        print(f"found day15_manifest_temp.txt in sources: {found_temp_source}")

        if not found_temp_source:
            raise AssertionError("temporary manifest test document was not retrieved")

        print("\n=== 4. 清理临时文件 ===")
        temp_file.unlink()
        service3.build_knowledge_base()
        print("cleanup completed")

    except Exception as error:
        print(f"Day 15 manifest test failed: {error}")
        raise

    finally:
        if temp_file.exists():
            temp_file.unlink()

        try:
            restore_service = service3 or create_service()
            restore_service.build_knowledge_base()
            print("formal knowledge base index restored")
        except Exception as restore_error:
            print(f"failed to restore formal index: {restore_error}")


if __name__ == "__main__":
    main()
