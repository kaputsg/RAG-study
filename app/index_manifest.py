import hashlib
import json
from pathlib import Path


def calculate_file_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with Path(file_path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def build_manifest(knowledge_base_dir: str | Path) -> dict:
    knowledge_base_path = Path(knowledge_base_dir)
    files = []

    for file_path in sorted(knowledge_base_path.glob("*.txt"), key=lambda path: path.name):
        if not file_path.is_file():
            continue

        stat = file_path.stat()
        files.append(
            {
                "filename": file_path.name,
                "path": str(file_path),
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "sha256": calculate_file_hash(file_path),
            }
        )

    return {
        "knowledge_base_dir": str(knowledge_base_path),
        "files": files,
    }


def save_manifest(manifest: dict, manifest_path: str | Path) -> None:
    manifest_path = Path(manifest_path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with manifest_path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)


def load_manifest(manifest_path: str | Path) -> dict:
    with Path(manifest_path).open("r", encoding="utf-8") as file:
        return json.load(file)


def manifest_matches(current_manifest: dict, saved_manifest: dict) -> bool:
    try:
        current_files = current_manifest["files"]
        saved_files = saved_manifest["files"]

        if not isinstance(current_files, list) or not isinstance(saved_files, list):
            return False

        if len(current_files) != len(saved_files):
            return False

        for current_file, saved_file in zip(current_files, saved_files):
            for key in ("filename", "size", "sha256"):
                if current_file.get(key) != saved_file.get(key):
                    return False

        return True
    except (KeyError, AttributeError, TypeError):
        return False


def has_manifest(manifest_path: str | Path) -> bool:
    return Path(manifest_path).is_file()
