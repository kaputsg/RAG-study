# RAG-study Docker 化后续规划

## 1. 为什么后续要 Docker 化

Docker 可以把后端运行环境、前端构建流程、环境变量和部署命令固定下来，减少不同机器之间的环境差异。对于 RAG-study 这类同时包含 Python 后端、Node.js 前端和本地运行时数据的项目，Docker 化后更方便迁移到云服务器或团队环境中运行。

Day 16 只做 Docker 规划，不正式 Docker 化。Dockerfile 和 docker-compose 可以放到后续 Day 17 再实现。

## 2. 后端 Dockerfile 计划

后端 Dockerfile 后续可以考虑：

* 使用 Python 官方基础镜像。
* 设置工作目录。
* 复制 `requirements.txt` 并安装依赖。
* 复制 `app/`、`data/knowledge_base/` 等运行所需文件。
* 通过环境变量注入 DeepSeek 配置。
* 使用 `python -m uvicorn app.api:app --host 0.0.0.0 --port 8000` 启动服务。

注意：后端镜像中不写入真实 API Key。

## 3. 前端 Dockerfile 或 Nginx 静态部署计划

前端后续有两种常见方案：

* 使用 Node.js 镜像执行 `npm install` 和 `npm run build`，生成 `frontend/dist/`。
* 使用 Nginx 镜像托管 `frontend/dist/` 静态文件。

如果使用多阶段构建，可以先在 Node.js 阶段打包，再把 `dist` 复制到 Nginx 阶段。

## 4. docker-compose 计划

后续 `docker-compose.yml` 可以包含：

* `backend` 服务：运行 FastAPI。
* `frontend` 服务：运行 Nginx 或静态文件服务。
* 网络配置：让前端能够访问后端服务。
* 端口映射：例如后端 `8000`、前端 `80`。
* 环境变量：通过 `.env` 或部署平台配置注入。
* 数据卷：挂载知识库和运行时索引目录。

## 5. 环境变量挂载

Docker 部署时需要把以下变量注入后端：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

前端构建时需要配置：

```env
VITE_API_BASE_URL=https://your-api-domain.com
```

真实 API Key 不写入镜像、不写入 Dockerfile、不提交 Git。

## 6. 数据目录挂载

后续 Docker 化时需要考虑挂载：

```text
data/knowledge_base/
data/vector_store/
logs/
```

原因：

* `data/knowledge_base/` 保存本地知识库 `.txt` 文档。
* `data/vector_store/` 保存 FAISS 索引、chunks 和 manifest 等运行时文件。
* `logs/` 保存 RAG 问答日志。

这些目录中的运行时产物不建议打进镜像，也不建议提交 Git。

## 7. 不适合现在一次性做完的原因

当前 Day 16 的目标是部署准备和文档整理，不是正式上线。现在不一次性完成 Docker 化，主要原因是：

* 需要先确认生产环境启动方式和环境变量边界。
* 需要先确认前端线上 API 地址配置方式。
* 需要先检查 CORS、运行时文件和敏感信息提交风险。
* Docker 化会引入 Dockerfile、docker-compose、镜像构建和数据卷策略，属于独立任务。
* 为了保持学习节奏，Dockerfile 和 docker-compose 更适合放到后续 Day 17 单独实现和验证。
