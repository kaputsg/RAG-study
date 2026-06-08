# RAG-study 部署准备说明

## 1. 文档说明

本文档用于 Day 16 的部署准备、生产环境配置和上线前检查说明。当前阶段只整理部署流程和注意事项，不表示项目已经正式上线，也不表示已经完成 Docker 化。

项目当前是一个本地知识库 RAG 问答系统，后端使用 FastAPI，前端使用 Vue 3 + Vite。部署时需要分别处理后端服务、前端静态资源、环境变量、运行时文件和安全检查。

## 2. 部署前准备

部署前先确认项目根目录中存在以下内容：

```text
README.md
.env.example
frontend/.env.example
app/api.py
frontend/package.json
docs/
data/
data/vector_store/
scripts/
```

还需要准备：

* Python 运行环境。
* Node.js 和 npm。
* DeepSeek API Key。
* 可以访问后端服务的服务器地址或域名。
* 用于部署前端静态文件的 Nginx、静态托管服务或其他 Web 服务。

## 3. 后端环境变量配置

后端本地配置文件是项目根目录下的 `.env`。可以参考 `.env.example` 创建，但不要提交 `.env`。

`.env` 示例只能使用占位值：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

说明：

* `DEEPSEEK_API_KEY` 需要填写自己的真实 Key，但真实 Key 不要写入 README、docs 或代码仓库。
* `DEEPSEEK_BASE_URL` 是 DeepSeek API 地址。
* `DEEPSEEK_MODEL` 是后端调用的模型名。
* `.env` 不提交 Git。

## 4. 后端依赖安装

在项目根目录执行：

```powershell
python -m pip install -r requirements.txt
```

如果使用虚拟环境，可以先创建并激活：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Python 虚拟环境目录不要提交 Git。

## 5. 后端开发环境启动

开发环境启动命令：

```powershell
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

说明：

* `--reload` 会在代码变化后自动重载，适合本地开发。
* `127.0.0.1` 只允许本机访问，适合本地调试。
* 启动后可以访问 `http://127.0.0.1:8000/health` 做健康检查。

## 6. 后端生产环境启动

基础生产启动方式：

```powershell
python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
```

说明：

* 这是基础生产启动方式。
* 生产环境不建议使用 `--reload`。
* `0.0.0.0` 可让服务器外部访问，需要配合防火墙、安全组、反向代理和域名配置。
* 更正式的生产部署可以继续使用 Nginx、进程守护工具、Docker 或云服务器部署。
* 当前 Day 16 只是部署准备，不是正式上线。

## 7. 前端环境变量配置

前端本地配置文件是 `frontend/.env.local`。可以参考 `frontend/.env.example` 创建，但不要提交 `frontend/.env.local`。

开发环境示例：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

生产环境示例：

```env
VITE_API_BASE_URL=https://your-api-domain.com
```

说明：

* `VITE_API_BASE_URL` 是前端请求 FastAPI 后端时使用的基础地址。
* 生产环境需要把它改成后端线上地址。
* `frontend/.env.local` 不提交 Git。

## 8. 前端开发环境启动

进入前端目录：

```powershell
cd frontend
```

安装依赖：

```powershell
npm install
```

启动 Vite 开发服务器：

```powershell
npm run dev
```

默认访问地址通常是：

```text
http://localhost:5173
```

## 9. 前端生产打包

进入前端目录：

```powershell
cd frontend
```

运行生产打包：

```powershell
npm run build
```

如果成功，会生成：

```text
frontend/dist/
```

说明：

* `dist` 是构建产物。
* `dist` 不提交 Git。
* 生产环境可以把 `frontend/dist/` 部署到 Nginx 或静态托管服务。
* 如果 build 失败，先检查 Node.js、`npm install`、环境变量和代码语法。

## 10. 前后端地址配置说明

开发环境常见组合：

```text
后端：http://127.0.0.1:8000
前端：http://localhost:5173
VITE_API_BASE_URL=http://127.0.0.1:8000
```

生产环境常见组合：

```text
后端：https://your-api-domain.com
前端：https://your-web-domain.com
VITE_API_BASE_URL=https://your-api-domain.com
```

注意：

* 前端页面地址和后端 API 地址可以不同。
* 前端打包时会读取 Vite 环境变量。
* 如果 `VITE_API_BASE_URL` 配错，页面能打开，但接口请求会失败。

## 11. CORS 配置说明

CORS（跨源资源共享）用于控制浏览器是否允许前端页面请求不同域名、端口或协议下的后端接口。

开发环境中，前端通常运行在 `http://localhost:5173`，后端运行在 `http://127.0.0.1:8000`，这属于跨源请求，需要后端允许对应来源。

生产环境不建议使用：

```python
allow_origins=["*"]
```

更推荐只允许真实前端域名，例如：

```python
allow_origins=["https://your-web-domain.com"]
```

本次 Day 16 不修改后端 CORS 代码，只说明上线前需要检查。

## 12. 运行时文件说明

以下文件或目录属于本地配置、运行时数据、缓存或构建产物，不提交 Git：

```text
.env
frontend/.env.local
data/vector_store/faiss.index
data/vector_store/chunks.json
data/vector_store/manifest.json
logs/rag_requests.jsonl
frontend/node_modules/
frontend/dist/
.venv/
.venv-1/
```

说明：

* `.env` 不提交。
* `frontend/.env.local` 不提交。
* `data/vector_store/faiss.index` 不提交。
* `data/vector_store/chunks.json` 不提交。
* `data/vector_store/manifest.json` 不提交。
* `logs/rag_requests.jsonl` 不提交。
* `frontend/node_modules` 不提交。
* `frontend/dist` 不提交。

## 13. 常见部署问题

### 13.1 后端没启动，前端请求失败

现象：前端页面可以打开，但提交问题、上传文档或加载文档列表失败。

检查：

```powershell
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

然后访问：

```text
http://127.0.0.1:8000/health
```

### 13.2 VITE_API_BASE_URL 配错

现象：前端请求打到错误地址，浏览器控制台出现网络错误或 404。

检查 `frontend/.env.local`：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

生产环境需要改为：

```env
VITE_API_BASE_URL=https://your-api-domain.com
```

### 13.3 DeepSeek API Key 没配置

现象：后端启动或问答接口调用失败，提示环境变量或模型调用异常。

检查根目录 `.env` 是否存在，并包含：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

真实 API Key 只写在本地 `.env` 或服务器环境变量中，不写入仓库。

### 13.4 CORS 拦截

现象：后端接口可以直接访问，但浏览器前端请求被拦截。

检查：

* 前端域名是否在后端 CORS 允许列表中。
* 生产环境是否避免使用过宽的 `allow_origins=["*"]`。
* 前端请求地址是否与实际后端地址一致。

### 13.5 上传文件不是 UTF-8

现象：上传 `.txt` 文件失败，接口提示编码不正确。

处理：

* 确认文件扩展名是 `.txt`。
* 使用编辑器把文件另存为 UTF-8 编码。
* 重新上传。

### 13.6 FAISS 索引文件不存在，首次启动较慢

现象：首次启动后端时等待时间较长。

原因：后端需要加载 BGE 模型、读取知识库、切分文本并建立 FAISS 索引。

处理：等待首次索引构建完成，再访问接口。

### 13.7 知识库文件变化后自动重建索引

现象：上传或删除文档后，接口响应时间变长。

原因：知识库文件变化会触发索引重建，确保后续问答使用最新文档内容。

处理：等待上传或删除接口完成，再继续提问。
