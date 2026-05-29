# RAG-study

一个基于 **DeepSeek API + BGE Embedding + FAISS + FastAPI + Vue** 的本地知识库 RAG 问答项目。

项目目标是实现一个完整的本地知识库问答系统：用户在前端输入问题，系统从本地知识库中检索相关资料，再调用大模型生成回答，并展示引用来源。

---

## 功能特点

* 支持读取本地 `txt` 知识库文档
* 支持文本切分 chunk，并保留来源信息
* 使用 BGE 中文 Embedding 模型生成文本向量
* 使用 FAISS 建立本地向量索引
* 支持相似度检索和阈值过滤
* 使用 DeepSeek API 生成最终回答
* 使用 FastAPI 提供后端 `/ask` 接口
* 使用 Vue 前端页面进行问答
* 前端展示模型回答和引用来源

---

## 技术栈

### 后端

* Python
* FastAPI
* DeepSeek API
* sentence-transformers
* BAAI/bge-small-zh-v1.5
* FAISS
* Pydantic
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
├── app/
│   ├── api.py
│   ├── config.py
│   ├── deepseek_client.py
│   ├── document_loader.py
│   ├── vector_store.py
│   └── rag_service.py
├── data/
│   └── knowledge_base/
│       ├── frontend_vue.txt
│       ├── python_backend.txt
│       └── rag_intro.txt
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   └── main.js
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
├── scripts/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 后端启动方式

### 1. 创建并激活虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 不允许执行脚本，可以执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

然后重新激活虚拟环境。

---

### 2. 安装后端依赖

```powershell
python -m pip install -r requirements.txt
```

---

### 3. 配置后端环境变量

在项目根目录新建 `.env` 文件：

```env
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

注意：`.env` 文件包含真实 API Key，不要提交到 GitHub 或 Gitee。

---

### 4. 启动后端服务

在项目根目录运行：

```powershell
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

后端地址：

```text
http://127.0.0.1:8000
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

健康检查：

```text
http://127.0.0.1:8000/health
```

---

## 前端启动方式

### 1. 进入前端目录

```powershell
cd frontend
```

---

### 2. 安装前端依赖

```powershell
npm install
```

---

### 3. 配置前端环境变量

在 `frontend/` 目录下新建 `.env.local` 文件：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

也可以参考：

```text
frontend/.env.example
```

注意：`frontend/.env.local` 是本地配置文件，不要提交。

---

### 4. 启动前端页面

```powershell
npm run dev
```

前端地址：

```text
http://localhost:5173
```

---

## API 说明

### GET `/`

用于测试后端服务是否启动。

响应示例：

```json
{
  "message": "RAG Knowledge Base API is running."
}
```

---

### GET `/health`

用于健康检查。

响应示例：

```json
{
  "status": "ok",
  "service": "rag-api"
}
```

---

### POST `/ask`

RAG 问答接口。

请求体：

```json
{
  "question": "开发 Python 后端 API 接口服务推荐用什么框架？"
}
```

响应示例：

```json
{
  "answer": "根据知识库资料，开发 Python 后端 API 接口服务推荐使用 FastAPI。",
  "sources": [
    {
      "source": "data\\knowledge_base\\python_backend.txt",
      "chunk_index": 1,
      "text": "如果要开发 Python 后端 API 服务，可以优先考虑 FastAPI。",
      "score": 0.7964
    }
  ]
}
```

如果知识库中没有相关信息，返回示例：

```json
{
  "answer": "我没有在知识库中找到相关信息。",
  "sources": []
}
```

如果问题为空，返回：

```json
{
  "detail": "question 不能为空"
}
```

---

## 当前知识库内容

当前示例知识库位于：

```text
data/knowledge_base/
```

包含：

```text
frontend_vue.txt
python_backend.txt
rag_intro.txt
```

可以继续添加更多 `.txt` 文件。添加后需要重启后端服务，让系统重新加载知识库并建立向量索引。

---

## 核心流程

```text
用户问题
↓
Vue 前端发送请求
↓
FastAPI /ask 接口
↓
RAGService
↓
DocumentLoader 读取并切分本地文档
↓
VectorStore 使用 BGE 生成 embedding
↓
FAISS 检索相关 chunks
↓
拼接 context
↓
DeepSeek 根据资料生成回答
↓
返回 answer 和 sources
```

---

## 已完成功能

* DeepSeek API 调用封装
* `.env` 配置读取
* API 错误处理和 retry 重试
* BGE Embedding 向量化
* FAISS 本地向量检索
* 本地 `txt` 文档加载
* chunk 切分和来源追踪
* RAGService 模块化封装
* FastAPI 后端接口
* `/ask` 问答接口
* `/health` 健康检查接口
* CORS 配置
* Pydantic 请求和响应模型
* 空问题校验和错误处理
* Vue 前端页面
* 前端 fetch 调用后端接口
* answer 和 sources 展示
* 引用来源折叠展示
* 前端 API 地址环境变量配置

---

## 后续优化方向

* 支持上传文档
* 支持更新知识库后重新构建索引
* 支持 PDF / Word / Markdown 文档解析
* 优化 chunk 切分策略
* 增加 rerank 重排序
* 增加混合检索
* 增加多轮对话历史
* 增加用户登录和权限控制
* 增加日志系统
* 增加 Docker 部署
* 增加线上部署说明

---

## 注意事项

* `.env` 不要提交到 GitHub 或 Gitee
* `frontend/.env.local` 不要提交
* `frontend/node_modules/` 不要提交
* `frontend/dist/` 不要提交
* 如果前端请求失败，请先确认后端服务是否启动
* 如果后端启动慢，通常是因为正在加载 BGE 模型和建立 FAISS 索引
