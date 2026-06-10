# RAG-study

## 项目简介

一个基于 **DeepSeek API + BGE Embedding + FAISS + FastAPI + Vue 3** 的本地知识库 RAG（Retrieval-Augmented Generation，检索增强生成）问答项目。

用户可以在前端页面中查看当前知识库文档、上传或删除 UTF-8 编码的 `.txt` 文档，并针对知识库内容提问。系统会先从本地知识库中检索相关文本片段，再调用 DeepSeek API 生成回答，同时返回引用来源，便于核对答案依据。

---

## 功能特点

### RAG 问答

* 读取本地 `.txt` 知识库文档
* 按固定长度切分 chunk，并保留 `source` 和 `chunk_index`
* 使用 `BAAI/bge-small-zh-v1.5` 生成中文文本向量
* 使用 FAISS 建立本地向量索引
* 通过相似度阈值过滤低相关结果
* 将检索结果作为 context 交给 DeepSeek API 生成回答
* 返回 `answer` 和 `sources` 引用来源

### 知识库文档管理

* 查看当前知识库文档列表
* 上传 UTF-8 编码的 `.txt` 文档
* 上传成功后自动重建 FAISS 索引
* 删除知识库中的 `.txt` 文档
* 删除成功后自动重建 FAISS 索引
* 前端自动展示和手动刷新文档列表
* 上传成功后自动刷新文档列表
* 删除文档前进行二次确认
* 删除过程中禁用对应按钮，避免重复提交
* 删除成功后自动刷新文档列表

---

## 技术栈

### 后端

* Python
* FastAPI
* Pydantic
* DeepSeek API
* sentence-transformers
* `BAAI/bge-small-zh-v1.5`
* FAISS
* python-dotenv
* tenacity

### 前端

* Vue 3
* Vite
* JavaScript
* Fetch API

---

## 项目结构

```text
RAG-study/
├─ app/
│  ├─ api.py                 # FastAPI 接口与知识库文档管理
│  ├─ config.py              # 环境变量读取与校验
│  ├─ deepseek_client.py     # DeepSeek API 调用与 retry
│  ├─ document_loader.py     # txt 文档读取与 chunk 切分
│  ├─ rag_service.py         # RAG 流程封装
│  └─ vector_store.py        # BGE embedding 与 FAISS 检索
├─ data/
│  └─ knowledge_base/        # 本地 txt 知识库
├─ docs/
│  ├─ demo_flow.md               # 项目演示流程
│  ├─ deployment_guide.md        # 部署准备说明
│  ├─ docker_guide.md            # Docker 启动指南
│  ├─ docker_plan.md             # Docker 化后续规划
│  ├─ production_checklist.md    # 上线前安全检查清单
│  └─ interview_qa.md            # 项目面试问答
├─ frontend/
│  ├─ src/
│  │  ├─ App.vue             # 问答、上传、列表和删除页面
│  │  └─ main.js
│  ├─ .env.example           # 前端环境变量示例
│  ├─ package.json
│  └─ vite.config.js
├─ scripts/
├─ .dockerignore             # Docker 构建忽略规则
├─ docker-compose.yml        # 本地后端容器启动配置
├─ Dockerfile                # FastAPI 后端容器镜像定义
├─ .env.example              # 后端环境变量示例
├─ requirements.txt
└─ README.md
```

---

## 后端启动方式

以下命令在项目根目录 `D:\Projects\RAG-study` 中执行。

### 1. 创建并激活虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 不允许执行激活脚本，可以在当前终端中执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### 2. 安装后端依赖

```powershell
python -m pip install -r requirements.txt
```

### 3. 配置环境变量

参考根目录下的 `.env.example` 创建本地 `.env` 文件，并填写自己的 API Key。不要提交真实 API Key。

### 4. 启动 FastAPI

```powershell
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

启动后可以访问：

```text
后端地址：http://127.0.0.1:8000
接口文档：http://127.0.0.1:8000/docs
健康检查：http://127.0.0.1:8000/health
```

首次启动时需要加载 BGE 模型并建立 FAISS 索引，耗时可能比普通接口服务更长。

---

## 前端启动方式

打开另一个 PowerShell 终端，进入前端目录：

```powershell
cd frontend
```

安装依赖：

```powershell
npm install
```

参考 `frontend/.env.example` 创建本地 `frontend/.env.local` 文件。

启动 Vite 开发服务器：

```powershell
npm run dev
```

默认访问地址：

```text
http://localhost:5173
```

---

## Docker 启动方式（Day 17）

Day 17 只 Docker 化 FastAPI 后端，不做前端 Nginx 容器，不表示项目已经正式上线。

详细说明见：

* [Docker 启动指南](docs/docker_guide.md)
* [Docker 化规划](docs/docker_plan.md)

### Docker 部署准备

启动前请确认：

* 已安装并启动 Docker Desktop。
* 项目根目录存在 `.env`。
* `.env` 中已经配置 DeepSeek API Key。
* `data/knowledge_base/` 中存在知识库 `.txt` 文件。

不要把真实 API Key 写入 `Dockerfile`、`docker-compose.yml` 或 README。

### 使用 docker build 和 docker run

在项目根目录执行：

```powershell
docker build -t rag-study-backend .
docker run --env-file .env -p 8000:8000 rag-study-backend
```

### 使用 docker compose

在项目根目录执行：

```powershell
docker compose up --build
```

停止容器：

```powershell
docker compose down
```

`docker-compose.yml` 会挂载以下本地目录：

```text
data/knowledge_base/
data/vector_store/
logs/
```

这样容器重启后，知识库、FAISS 索引和问答日志仍保留在本机项目目录中。

### 前端连接 Docker 后端

Day 17 前端仍可本地运行：

```powershell
cd frontend
npm run dev
```

前端 API 地址仍然指向本机后端端口：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

启动后可以访问：

```text
健康检查：http://127.0.0.1:8000/health
接口文档：http://127.0.0.1:8000/docs
```

---

## 部署准备

Day 16 整理部署准备、生产环境配置说明和上线前检查清单。Day 17 完成后端 Docker 化初步实现，但只覆盖本地后端容器启动，不表示项目已经正式上线。

### 开发环境启动

开发环境适合本地调试，后端建议使用 `--reload`，代码变更后会自动重载：

```powershell
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

前端开发环境启动：

```powershell
cd frontend
npm run dev
```

说明：

* `--reload` 适合开发环境，不建议生产环境使用。
* `127.0.0.1` 只允许本机访问，适合本地调试。
* 前端开发服务通常运行在 `http://localhost:5173`。

### 生产环境启动

后端基础生产启动示例：

```powershell
python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
```

说明：

* 生产环境后端启动命令不建议使用 `--reload`。
* `0.0.0.0` 可让服务器外部访问，需要配合服务器防火墙、安全组和反向代理配置。
* 更正式的生产部署可以继续接入 Nginx、进程守护工具、Docker 或云服务器部署。

前端生产打包：

```powershell
cd frontend
npm run build
```

如果打包成功，会生成：

```text
frontend/dist/
```

说明：

* `frontend/dist/` 是前端构建产物，不提交 Git。
* 生产环境可以把 `frontend/dist/` 部署到 Nginx 或静态托管服务。
* 前端生产环境需要配置 `VITE_API_BASE_URL` 为后端线上地址。
* 如果 `npm run build` 失败，先检查 Node.js、`npm install`、环境变量和代码语法。

### 部署相关文档

* [部署准备说明](docs/deployment_guide.md)
* [上线前安全检查清单](docs/production_checklist.md)
* [Docker 启动指南](docs/docker_guide.md)
* [Docker 化规划](docs/docker_plan.md)

---

## 环境变量配置

### 后端 `.env`

参考 `.env.example`：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

字段说明：

| 字段 | 说明 |
| --- | --- |
| `DEEPSEEK_API_KEY` | DeepSeek API Key。本地 `.env` 中需要填写自己的值 |
| `DEEPSEEK_BASE_URL` | DeepSeek API 地址 |
| `DEEPSEEK_MODEL` | 调用的模型名 |

### 前端 `frontend/.env.local`

参考 `frontend/.env.example`：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

字段说明：

| 字段 | 说明 |
| --- | --- |
| `VITE_API_BASE_URL` | 前端请求 FastAPI 后端时使用的基础地址 |

---

## API 说明

### GET `/`

**功能说明**

用于确认后端服务是否已启动。

**请求示例**

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/"
```

**响应示例**

```json
{
  "message": "RAG Knowledge Base API is running."
}
```

---

### GET `/health`

**功能说明**

用于执行基础健康检查。

**请求示例**

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health"
```

**响应示例**

```json
{
  "status": "ok",
  "service": "rag-api"
}
```

---

### POST `/ask`

**功能说明**

接收用户问题，执行向量检索，将相关 chunks 作为 context 传给 DeepSeek API，并返回回答和引用来源。

**请求示例**

```powershell
$body = @{
    question = "开发 Python 后端 API 接口服务推荐用什么框架？"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/ask" `
    -ContentType "application/json" `
    -Body $body
```

请求体：

```json
{
  "question": "开发 Python 后端 API 接口服务推荐用什么框架？"
}
```

**响应示例**

```json
{
  "answer": "根据知识库资料，开发 Python 后端 API 服务可以优先考虑 FastAPI。",
  "sources": [
    {
      "source": "data\\knowledge_base\\python_backend.txt",
      "chunk_index": 1,
      "text": "在 Web 后端开发中，FastAPI 是一个常见的 Python 框架。它适合开发 API 接口服务，支持自动生成接口文档，并且性能较好。",
      "score": 0.7964
    }
  ]
}
```

当没有检索到高于相似度阈值的内容时，响应示例：

```json
{
  "answer": "抱歉，我无法找到相关信息来回答您的问题。",
  "sources": []
}
```

**常见错误**

| 状态码 | 情况 |
| --- | --- |
| `400` | `question` 仅包含空白字符 |
| `422` | 请求体缺少 `question`，或 `question` 为空字符串 |
| `500` | RAG 服务调用异常 |

---

### GET `/documents`

**功能说明**

返回 `data/knowledge_base/` 中当前存在的 `.txt` 文档列表。前端会在页面加载、上传成功和删除成功后调用该接口刷新列表。

**请求示例**

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/documents"
```

**响应示例**

```json
{
  "documents": [
    {
      "filename": "python_backend.txt",
      "path": "data\\knowledge_base\\python_backend.txt",
      "size": 385
    }
  ]
}
```

---

### POST `/documents/upload`

**功能说明**

上传一个 UTF-8 编码的 `.txt` 文件到本地知识库。上传成功后，后端会重新读取全部知识库文档、切分 chunks，并重建 FAISS 索引。

**请求示例**

PowerShell 7 或更高版本：

```powershell
curl.exe `
    -X POST `
    -F "file=@D:\temp\database_transaction_demo.txt" `
    "http://127.0.0.1:8000/documents/upload"
```

请求类型：

```text
multipart/form-data
```

**响应示例**

```json
{
  "filename": "database_transaction_demo.txt",
  "message": "文档上传成功，知识库索引已重建",
  "chunk_count": 12
}
```

**常见错误**

| 状态码 | 情况 |
| --- | --- |
| `400` | 文件名为空 |
| `400` | 文件扩展名不是 `.txt` |
| `400` | 文件不是 UTF-8 编码 |
| `400` | 文件内容为空 |
| `500` | 知识库索引重建失败 |

---

### DELETE `/documents/{filename}`

**功能说明**

删除知识库中的指定 `.txt` 文件。删除成功后，后端会重新读取剩余文档并重建 FAISS 索引。

**请求示例**

```powershell
Invoke-RestMethod `
    -Method Delete `
    -Uri "http://127.0.0.1:8000/documents/database_transaction_demo.txt"
```

**响应示例**

```json
{
  "filename": "database_transaction_demo.txt",
  "message": "文档删除成功，知识库索引已重建",
  "chunk_count": 9
}
```

**常见错误**

| 状态码 | 情况 |
| --- | --- |
| `400` | 文件扩展名不是 `.txt` |
| `400` | 目标不是有效文件 |
| `404` | 文件不存在 |
| `500` | 知识库索引重建失败 |

---

## 当前知识库说明

本地知识库目录：

```text
data/knowledge_base/
```

当前示例文档：

```text
ai_tools_intro.txt
frontend_vue.txt
python_backend.txt
rag_intro.txt
```

目前只支持 UTF-8 编码的 `.txt` 文档，不支持 PDF、Word 或其他格式。可以通过前端页面上传和删除文档，也可以调用对应 API。上传或删除后，后端会自动重建索引，不需要手动重启服务。

---

## 核心流程

### 问答流程

```text
用户输入问题
→ Vue 前端调用 POST /ask
→ FastAPI 接收并校验问题
→ RAGService 调用 VectorStore.search()
→ BGE 将问题转换成 embedding
→ FAISS 检索相似 chunks
→ similarity_threshold 过滤低相关结果
→ RAGService 拼接 context
→ DeepSeek API 根据 context 生成回答
→ 后端返回 answer 和 sources
→ 前端展示回答、来源文件、chunk_index、相似度和片段内容
```

### 文档管理流程

```text
前端上传或删除 txt 文档
→ FastAPI 校验请求
→ 更新 data/knowledge_base/
→ DocumentLoader 重新读取全部 txt 文档
→ 重新切分 chunks
→ BGE 重新生成 embeddings
→ FAISS 重建本地索引
→ 前端自动刷新文档列表
```

---

## 已完成功能

### Day 1 - Day 9：基础 RAG 问答

* DeepSeek API 调用封装
* `.env` 配置管理
* API 错误处理和 retry
* BGE 中文 embedding
* FAISS 本地向量检索
* 本地 `.txt` 知识库读取和 chunk 切分
* `source` 和 `chunk_index` 来源追踪
* `RAGService` 模块化封装
* FastAPI 后端接口
* Vue 前端页面
* 前端 loading 和 error 状态
* `answer` 和 `sources` 引用来源展示
* 前端 API 地址环境变量配置

### Day 10：文档上传与索引重建

* 上传 UTF-8 编码的 `.txt` 文档
* `POST /documents/upload` 上传接口
* 上传成功后自动重建 FAISS 索引
* 前端上传状态和结果提示

### Day 11：文档列表与删除

* `GET /documents` 文档列表接口
* `DELETE /documents/{filename}` 文档删除接口
* 前端展示当前知识库文档列表
* 上传成功后自动刷新文档列表
* 支持手动刷新文档列表
* 删除文档前二次确认
* 删除过程中禁用对应按钮
* 删除成功后自动刷新文档列表
* 删除成功后自动重建 FAISS 索引

---

## 后续优化方向

* 增加 PDF、Word、Markdown 等文档解析能力
* 优化 chunk 切分策略，例如按段落或语义切分
* 增加 rerank（重排序）步骤，提高检索准确率
* 增加关键词与向量结合的混合检索
* 支持增量更新索引，避免每次上传或删除都全量重建
* 将向量索引持久化，减少服务重启时的初始化时间
* 增加文档覆盖、删除和索引重建失败时的事务处理
* 增加日志、测试、用户权限和 Docker 部署配置

---

## 注意事项

* `.env` 中包含真实 API Key，不要提交到 GitHub 或 Gitee。
* `frontend/.env.local` 是本地配置文件，不要提交。
* `frontend/node_modules/` 和 `frontend/dist/` 不要提交。
* Day 17 只 Docker 化后端，不包含前端 Nginx 容器、HTTPS、域名或线上服务器部署。
* Docker 启动时通过 `.env` 注入环境变量，不要把真实 API Key 写进镜像或 compose 文件。
* 使用 `docker compose` 启动时，`data/knowledge_base/`、`data/vector_store/` 和 `logs/` 会通过 volume 挂载保留。
* 当前仅支持 UTF-8 编码的 `.txt` 文档。
* 上传同名 `.txt` 文件会覆盖知识库中的同名文件。
* 上传和删除文档会触发全量索引重建，文档较多时耗时会增加。
* 后端启动时会加载 BGE 模型并建立 FAISS 索引，首次启动可能较慢。
* 如果前端请求失败，请先检查后端是否已启动，以及 `VITE_API_BASE_URL` 是否正确。
* 当前项目用于本地学习和演示，已经实现基础索引持久化，但还没有生产环境所需的鉴权、增量索引和完整事务处理。

---

## 演示与面试资料

* [项目演示流程](docs/demo_flow.md)
* [项目面试问答](docs/interview_qa.md)
* [部署准备说明](docs/deployment_guide.md)
* [上线前安全检查清单](docs/production_checklist.md)
* [Docker 启动指南](docs/docker_guide.md)
* [Docker 化规划](docs/docker_plan.md)

### 项目展示与最终验收

* [项目最终验收清单](docs/final_acceptance_checklist.md)：逐项检查本地环境、RAG、文档管理、索引、日志、Docker 和 Git 安全。
* [最终项目演示脚本](docs/final_demo_script.md)：适合录屏、答辩和面试的完整演示顺序与异常处理。
* [项目讲解稿](docs/project_pitch.md)：包含 30 秒、1 分钟、2 分钟和面试口语版本。
* [简历项目描述](docs/resume_project.md)：提供中英文简历、STAR 描述和常见追问回答。
* [社交平台展示文案](docs/social_post.md)：提供短视频、小红书、粉丝群和 GitHub 发布文案。
