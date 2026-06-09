# RAG-study Docker 启动指南

## 1. 文档说明

本文档记录 RAG-study 在 Day 17 阶段的 Docker 化启动方式，面向第一次使用 Docker 启动本项目的同学。

Day 17 的目标是先把 FastAPI 后端放进 Docker 容器中运行，并通过 volume 保留知识库、向量索引和日志。本文不包含正式线上部署流程。

## 2. Day 17 Docker 化范围

Day 17 只 Docker 化 FastAPI 后端：

* 新增后端 `Dockerfile`。
* 新增 `.dockerignore`。
* 新增 `docker-compose.yml`，只包含 `backend` 服务。
* 使用本地 `.env` 注入 DeepSeek 配置。
* 挂载 `data/knowledge_base/`、`data/vector_store/` 和 `logs/`。

Day 17 不做：

* 前端 Nginx 容器。
* Nginx 反向代理。
* HTTPS。
* 域名配置。
* 线上服务器部署。

## 3. 前置条件

启动前请确认：

* 已安装 Docker Desktop，并且 Docker Desktop 正在运行。
* 当前命令行位于项目根目录。
* 项目根目录存在 `.env`。
* `.env` 中已经配置 DeepSeek API Key。
* `data/knowledge_base/` 存在知识库 `.txt` 文件。

可以先访问项目根目录：

```powershell
cd D:\Projects\RAG-study
```

## 4. Dockerfile 说明

根目录 `Dockerfile` 使用 `python:3.11-slim` 作为基础镜像。

主要步骤：

* 设置容器工作目录为 `/app`。
* 设置 `PYTHONDONTWRITEBYTECODE=1`，避免生成 `.pyc` 文件。
* 设置 `PYTHONUNBUFFERED=1`，让日志更及时输出。
* 复制 `requirements.txt` 并安装 Python 依赖。
* 复制项目文件到 `/app`。
* 暴露后端端口 `8000`。
* 使用以下命令启动 FastAPI：

```powershell
python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
```

Docker 环境不使用 `--reload`。

## 5. .dockerignore 说明

根目录 `.dockerignore` 用来减少 Docker build 上下文，并避免敏感文件和运行时文件被复制进镜像。

当前会忽略：

* `.venv/`、`.venv-1/`
* Python 缓存和 `.pyc` 文件
* `.git/`、`.gitignore`
* `.env`
* `frontend/node_modules/`
* `frontend/dist/`
* `logs/*.jsonl`、`logs/*.log`
* `data/vector_store/*.index`、`data/vector_store/*.json`
* `AGENTS.md`
* `.pytest_cache/`、`.mypy_cache/`、`.vscode/`、`.idea/`

注意：

* 不忽略 `data/knowledge_base/`，因为容器需要能看到示例知识库。
* 不忽略 `data/vector_store/.gitkeep`。
* 不忽略 `logs/.gitkeep`。
* `.env` 不会被打进镜像，运行时通过 `--env-file .env` 或 `env_file` 注入。

## 6. docker-compose.yml 说明

根目录 `docker-compose.yml` 只定义一个服务：`backend`。

它会：

* 使用当前目录构建镜像。
* 使用 `Dockerfile`。
* 将容器命名为 `rag-study-backend`。
* 映射端口 `8000:8000`。
* 从 `.env` 读取环境变量。
* 挂载本地数据目录。
* 使用 `restart: unless-stopped`。

当前没有定义前端容器，也没有定义数据库容器。

## 7. 环境变量准备

请在项目根目录准备 `.env` 文件，可以参考 `.env.example`。

示例字段：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

不要把真实 API Key 写进 `Dockerfile`、`docker-compose.yml` 或 README。

## 8. 使用 docker build 启动后端

在项目根目录构建镜像：

```powershell
docker build -t rag-study-backend .
```

构建完成后启动容器：

```powershell
docker run --env-file .env -p 8000:8000 rag-study-backend
```

这种方式适合快速验证镜像是否能启动。

如果希望容器重启后仍保留知识库、索引和日志，推荐使用 `docker compose`，因为 compose 文件已经配置了 volume。

## 9. 使用 docker compose 启动后端

在项目根目录执行：

```powershell
docker compose up --build
```

停止并移除容器：

```powershell
docker compose down
```

如果只想后台运行，可以使用：

```powershell
docker compose up --build -d
```

## 10. 测试接口

启动后访问：

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

PowerShell 测试健康检查：

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health"
```

如果返回 `status` 为 `ok`，说明后端服务已经启动。

## 11. 前端如何连接 Docker 后端

Day 17 不做前端容器。前端仍然本地运行 Vite 开发服务器。

在 `frontend/.env.local` 中配置：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

然后启动前端：

```powershell
cd frontend
npm run dev
```

前端页面会通过 `VITE_API_BASE_URL` 访问 Docker 中运行的后端。

## 12. 数据目录挂载说明

`docker-compose.yml` 挂载了三个目录：

```yaml
volumes:
  - ./data/knowledge_base:/app/data/knowledge_base
  - ./data/vector_store:/app/data/vector_store
  - ./logs:/app/logs
```

作用：

* `data/knowledge_base/` 保存本地知识库 `.txt` 文件。
* `data/vector_store/` 保存 FAISS 索引、chunks 和 manifest 等运行时文件。
* `logs/` 保存 RAG 问答日志。

这样容器重启后，知识库、索引和日志仍保留在本机项目目录中。

## 13. 模型下载和首次启动较慢说明

后端启动时会加载 BGE embedding 模型，并检查或构建 FAISS 索引。

首次启动可能较慢，常见原因：

* 本机还没有缓存 `BAAI/bge-small-zh-v1.5` 模型。
* Docker 容器需要下载 HuggingFace 模型文件。
* 知识库文档较多，需要生成 embedding 并构建索引。
* 国内网络访问 HuggingFace 可能较慢。

如果首次启动耗时较长，先观察容器日志，不要马上判定为启动失败。

## 14. 常见问题

### 1. Docker 没安装或没启动

如果命令行提示找不到 `docker`，或者无法连接 Docker daemon，请先安装并启动 Docker Desktop。

### 2. .env 缺失

`docker run --env-file .env` 和 `docker compose up --build` 都依赖项目根目录的 `.env`。如果缺失，请参考 `.env.example` 创建。

### 3. DeepSeek API Key 未配置

如果 `.env` 中没有配置 `DEEPSEEK_API_KEY`，后端调用 DeepSeek 时会失败。请填写自己的 API Key，不要提交到 Git。

### 4. 首次启动很慢

首次启动需要加载或下载 BGE embedding 模型，也可能需要构建 FAISS 索引。请先查看日志并等待。

### 5. 国内网络下载 HuggingFace 模型慢

如果卡在模型下载阶段，通常是网络问题。后续可以考虑模型缓存优化或提前准备模型缓存，Day 17 暂不展开。

### 6. 端口 8000 被占用

如果本机已经有服务占用 8000 端口，容器会启动失败。可以先停止占用端口的服务，或者临时调整端口映射。

### 7. 前端请求失败

检查 `frontend/.env.local` 是否配置：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

修改后需要重启前端开发服务器。

### 8. data/vector_store 没有索引

如果 `data/vector_store/` 中没有索引文件，后端首次启动或知识库变化时会自动构建。

### 9. logs 没有日志

RAG 问答日志通常在调用 `/ask` 后产生。只访问 `/health` 或 `/docs` 不一定会产生问答日志。

### 10. 容器重启后数据是否保留

使用 `docker compose` 启动时，知识库、索引和日志通过 volume 挂载到本地目录，容器重启后仍会保留。

## 15. 后续优化方向

后续可以继续考虑：

* 前端 Nginx 容器。
* Nginx 反向代理。
* HTTPS。
* 线上服务器部署。
* 模型缓存优化。
* 更细的镜像体积优化。
* 容器健康检查。
* 生产环境日志轮转和权限控制。

这些不属于 Day 17 的实现范围。
