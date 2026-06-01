"""
FastAPI 后端接口模块。

职责：
1. 创建 FastAPI 应用
2. 初始化 RAGService
3. 提供 /ask 接口
4. 返回模型回答和引用来源
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.rag_service import RAGService


# 创建 FastAPI 应用
app = FastAPI(
    title="RAG Knowledge Base API",
    description="本地知识库 RAG 问答接口",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KNOWLEDGE_BASE_DIR = Path("data/knowledge_base")
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)


# 初始化 RAG 服务
# 注意：这里会加载 BGE 模型、读取文档、建立 FAISS 索引，第一次启动会慢一点
rag_service = RAGService(
    knowledge_base_dir=str(KNOWLEDGE_BASE_DIR),
    chunk_size=120,
    chunk_overlap=30,
    top_k=3,
    similarity_threshold=0.65
)


class AskRequest(BaseModel):
    """
    /ask 接口的请求体格式。
    """

    question: str = Field(..., min_length=1, description="用户问题")

class UploadDocumentResponse(BaseModel):
    filename: str
    message: str
    chunk_count: int

class DeleteDocumentResponse(BaseModel):
    filename: str
    message: str
    chunk_count: int

class DocumentItem(BaseModel):
    filename: str
    path: str
    size: int


class DocumentListResponse(BaseModel):
    documents: list[DocumentItem]

class SourceItem(BaseModel):
    source: str
    chunk_index: int
    text: str
    score: float


class AskResponse(BaseModel):
    """
    /ask 接口的响应格式。
    """

    answer: str
    sources: list[SourceItem]


@app.get("/")
def root():
    """
    测试服务是否启动。
    """

    return {
        "message": "RAG Knowledge Base API is running."
    }

@app.get("/health")
def health_check():
    """
    健康检查接口。
    """

    return {
        "status": "ok",
        "service": "rag-api"
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """
    RAG 问答接口。
    """

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="question 不能为空"
        )

    try:
        result = rag_service.ask(question)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG 服务调用失败：{e}"
        )

@app.post("/documents/upload", response_model=UploadDocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    上传 txt 文档到知识库，并重新构建 RAG 索引。
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="文件名不能为空"
        )

    safe_filename = Path(file.filename).name

    if not safe_filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="目前只支持上传 .txt 文件"
        )

    content = await file.read()

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="文件编码必须是 UTF-8"
        )

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="上传文件内容不能为空"
        )

    file_path = KNOWLEDGE_BASE_DIR / safe_filename
    file_path.write_text(text, encoding="utf-8")

    try:
        rag_service.build_knowledge_base()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"知识库索引重建失败：{e}"
        )

    return {
        "filename": safe_filename,
        "message": "文档上传成功，知识库索引已重建",
        "chunk_count": len(rag_service.chunks)
    }

@app.get("/documents", response_model=DocumentListResponse)
def list_documents():
    """
    查看当前知识库中的 txt 文档列表。
    """

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):
        document_item = DocumentItem(
            filename=file_path.name,
            path=str(file_path),
            size=file_path.stat().st_size
        )
        documents.append(document_item)

    return {
        "documents": documents
    }

@app.delete("/documents/{filename}", response_model=DeleteDocumentResponse)
def delete_document(filename: str):
    """
    删除知识库中的 txt 文档，并重新构建 RAG 索引。
    """

    safe_filename = Path(filename).name

    if not safe_filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="目前只支持删除 .txt 文件"
        )

    file_path = KNOWLEDGE_BASE_DIR / safe_filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="目标不是有效文件"
        )

    file_path.unlink()

    try:
        rag_service.build_knowledge_base()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"知识库索引重建失败：{e}"
        )

    return {
        "filename": safe_filename,
        "message": "文档删除成功，知识库索引已重建",
        "chunk_count": len(rag_service.chunks)
    }
