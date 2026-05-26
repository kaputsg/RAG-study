"""
FastAPI 后端接口模块。

职责：
1. 创建 FastAPI 应用
2. 初始化 RAGService
3. 提供 /ask 接口
4. 返回模型回答和引用来源
"""

from fastapi import FastAPI, HTTPException
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


# 初始化 RAG 服务
# 注意：这里会加载 BGE 模型、读取文档、建立 FAISS 索引，第一次启动会慢一点
rag_service = RAGService(
    knowledge_base_dir="data/knowledge_base",
    chunk_size=120,
    chunk_overlap=30,
    top_k=3,
    similarity_threshold=0.65
)


class AskRequest(BaseModel):
    """
    /ask 接口的请求体格式。
    """

    # TODO 1：定义 question 字段，类型是 str
    question: str = Field(..., min_length=1, description="用户问题")

class SourceItem(BaseModel):
    source: str
    chunk_index: int
    text: str
    score: float


class AskResponse(BaseModel):
    """
    /ask 接口的响应格式。
    """

    # TODO 2：定义 answer 字段，类型是 str
    # TODO 3：定义 sources 字段，类型是 list
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