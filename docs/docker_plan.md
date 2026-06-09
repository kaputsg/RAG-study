# RAG-study Docker 化规划

## 1. 当前状态

Day 17 已完成 Docker 化初步实现，但只覆盖 FastAPI 后端容器的本地启动方案。

当前已经完成：

* 后端 `Dockerfile`。
* `.dockerignore`。
* `docker-compose.yml`。
* 后端容器本地启动方案。
* Docker 启动说明文档：`docs/docker_guide.md`。

当前没有正式上线，也没有完成线上生产部署。

## 2. Day 17 已完成内容

### 后端 Dockerfile

根目录 `Dockerfile` 使用 `python:3.11-slim` 作为基础镜像，安装 `requirements.txt` 中的依赖，并通过以下命令启动 FastAPI：

```powershell
python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
```

Docker 环境不使用 `--reload`。

### .dockerignore

根目录 `.dockerignore` 用于避免把虚拟环境、Git 目录、真实 `.env`、前端构建产物、日志文件和向量索引运行时文件复制进镜像。

保留：

* `data/knowledge_base/`
* `data/vector_store/.gitkeep`
* `logs/.gitkeep`

### docker-compose.yml

根目录 `docker-compose.yml` 只定义一个 `backend` 服务。

它会：

* 使用当前目录构建后端镜像。
* 映射端口 `8000:8000`。
* 通过 `.env` 注入环境变量。
* 挂载 `data/knowledge_base/`、`data/vector_store/` 和 `logs/`。
* 使用 `restart: unless-stopped`。

### 后端容器本地启动方案

可以直接构建镜像：

```powershell
docker build -t rag-study-backend .
docker run --env-file .env -p 8000:8000 rag-study-backend
```

也可以使用 Docker Compose：

```powershell
docker compose up --build
```

停止：

```powershell
docker compose down
```

## 3. Day 17 没有完成的内容

以下内容仍属于后续任务：

* 前端 Nginx 容器。
* Nginx 反向代理。
* HTTPS。
* 线上服务器部署。
* 模型缓存优化。

## 4. 为什么 Day 17 不做前端 Nginx 容器

当前阶段的目标是先验证后端容器能稳定启动，并确认 `.env`、知识库目录、向量索引目录和日志目录的边界。

前端仍使用本地 Vite 开发服务器：

```powershell
cd frontend
npm run dev
```

前端通过以下环境变量访问 Docker 后端：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 5. 数据目录挂载规划

后端容器需要保留三类本地数据：

```text
data/knowledge_base/
data/vector_store/
logs/
```

原因：

* `data/knowledge_base/` 保存本地知识库 `.txt` 文档。
* `data/vector_store/` 保存 FAISS 索引、chunks 和 manifest 等运行时文件。
* `logs/` 保存 RAG 问答日志。

这些目录通过 volume 挂载到容器中，避免容器重启后丢失运行时数据。

## 6. 后续优化方向

后续可以按独立任务继续推进：

* 增加前端 Nginx 容器。
* 增加 Nginx 反向代理。
* 配置 HTTPS。
* 部署到线上服务器。
* 优化 HuggingFace / BGE 模型缓存。
* 增加 Docker healthcheck。
* 优化镜像体积和构建缓存。

这些内容不属于 Day 17 初步实现范围。
