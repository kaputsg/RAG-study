# RAG-study 最终项目演示脚本

这份脚本适合录屏、课程答辩和面试现场演示。完整流程建议控制在 8 到 12 分钟，并提前准备一个 UTF-8 编码的临时 `.txt` 文档。

## 一、准备阶段

### 1. 演示材料

- 打开 GitHub 或 Gitee 项目主页，提前确认 README 可以正常浏览。
- 准备测试文档 `database_transaction_demo.txt`，内容简要说明数据库事务的 ACID 特性。
- 确认测试文档位于知识库目录之外，避免演示前已经被索引。
- 检查 `.env` 已配置，但录屏和投屏时不要展示真实 API Key。
- 清理浏览器中可能暴露隐私的信息，并放大终端与浏览器字号。

### 2. 启动后端

在项目根目录执行：

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

检查：

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### 3. 启动前端

另开一个 PowerShell：

```powershell
cd frontend
npm run dev
```

浏览器访问：

```text
http://localhost:5173
```

## 二、演示主流程

### 步骤 1：展示项目主页并介绍定位

打开 GitHub 或 Gitee 项目主页，指向 README，用一句话介绍：

> 这是一个基于 FastAPI、Vue、BGE、FAISS 和 DeepSeek API 的本地知识库 RAG 问答系统，重点完成了从文档检索、模型回答到来源展示和文档管理的完整流程。

补充说明：当前是本地学习和演示项目，只支持 UTF-8 `.txt` 文档，不是已经上线的完整 SaaS。

### 步骤 2：展示后端和前端启动状态

展示 FastAPI 启动终端、`/health` 和 `/docs`，再切换到 Vue 前端页面。说明 FastAPI 提供问答与文档管理接口，Vue 负责交互和结果展示。

### 步骤 3：展示当前知识库文档列表

在前端展示当前文档列表，并说明页面通过 `GET /documents` 获取本地知识库中的 `.txt` 文件。

### 步骤 4：提问已知问题

输入：

```text
开发 Python 后端 API 接口服务推荐用什么框架？
```

提交后依次展示：

1. `answer`：DeepSeek API 基于检索上下文生成的回答。
2. `sources`：引用的文件、`chunk_index`、`score` 和原始片段。
3. `retrieval_info`：`hit`、`max_score`、`source_count` 和 `confidence`。

讲解：

> 系统先用 BGE 将问题向量化，再通过 FAISS 检索相关 chunks。检索结果通过阈值过滤后交给 DeepSeek API，最终把回答、引用来源和检索质量一起返回。

### 步骤 5：上传测试文档

上传提前准备的 `database_transaction_demo.txt`。说明当前只接受 UTF-8 `.txt` 文件，上传成功后后端会重建索引。

### 步骤 6：展示列表自动刷新

上传成功后不要手动刷新，直接展示测试文档已经出现在列表中。说明前端会再次请求 `GET /documents`，同步后端状态。

### 步骤 7：提问新文档问题

输入：

```text
数据库事务的 ACID 是什么？
```

展示回答及来源，确认 `sources` 中包含 `database_transaction_demo.txt`。

### 步骤 8：删除测试文档

点击删除，展示二次确认和删除中的禁用状态。确认删除后，说明后端会删除文件并重建索引。

### 步骤 9：展示删除后自动刷新

确认测试文档自动从列表消失。必要时再次提问 ACID 问题，说明结果取决于剩余知识库是否还有相关资料；知识库没有相关资料时，系统应拒答或显示低置信度，而不是强行保证答案正确。

### 步骤 10：展示日志与评估

打开或说明：

```text
logs/rag_requests.jsonl
```

说明日志记录问题、回答结果和检索信息，便于排查和复盘。不要在公开录屏中展示敏感问题内容。

根据时间选择运行或说明：

```powershell
python -m scripts.day13_test_api
python -m scripts.day13_eval_questions
```

说明评估问题集用于检查已知问题命中、未知问题拒答和检索质量，不代表已经达到生产级自动评测。

### 步骤 11：说明索引持久化与 manifest

展示或说明运行时文件：

```text
data/vector_store/faiss.index
data/vector_store/chunks.json
data/vector_store/manifest.json
```

讲解：

> FAISS 索引和 chunks 会持久化到本地，后端再次启动时优先加载已有索引。manifest 用于记录知识库文件状态；如果文档发生变化，系统会检测不一致并重新构建索引。

### 步骤 12：说明 Docker 后端启动方式

展示 README 或 Docker 文档中的命令：

```powershell
docker build -t rag-study-backend .
docker run --env-file .env -p 8000:8000 rag-study-backend
docker compose up --build
```

明确说明：当前完成的是后端容器化初步实现，前端仍可在本地启动，不要描述成已经正式上线。

### 步骤 13：总结项目

> 项目亮点是完整走通了 RAG 问答、来源展示、检索质量、文档管理、日志评估、索引持久化和 Docker 后端容器化。当前不足是只支持 txt、切片策略较基础、文档变化后仍采用全量重建，也没有鉴权和完整生产部署。

## 三、演示重点

- RAG 不是让模型直接自由回答，而是“先检索，再基于资料生成”。
- `sources` 提供回答依据，但不能承诺完全消除大模型误差。
- `retrieval_info` 用于观察是否命中、最高分、来源数量和置信度。
- 上传和删除会同步更新文件、索引与前端列表。
- 持久化索引减少重复构建，manifest 保证知识库与索引的一致性。
- 日志与评估脚本让项目不只“能运行”，还具备基础可测试性。
- Docker 目前覆盖后端，不等于完整线上部署。

### 推荐演示问题

- 开发 Python 后端 API 接口服务推荐用什么框架？
- RAG 的基本流程是什么？
- Vue 在这个项目中负责什么？
- AI 工具调用常用于哪些场景？
- 数据库事务的 ACID 是什么？

## 四、异常情况处理

### 后端无法访问

先检查 `http://127.0.0.1:8000/health`，再检查虚拟环境、依赖和端口占用。不要在现场反复盲目重启。

### 前端请求失败

确认后端已启动，并检查 `frontend/.env.local` 中的 `VITE_API_BASE_URL`。修改环境变量后需重新运行 `npm run dev`。

### 首次启动较慢

BGE 模型首次加载可能需要时间。提前预热，并准备说明本地 embedding 模型加载和索引初始化过程。

### 上传失败

确认文件扩展名是 `.txt`、编码为 UTF-8、内容非空，且文件名符合要求。

### 回答不符合预期

先展开 `sources` 和 `retrieval_info` 判断是检索问题还是生成问题。知识库没有相关资料时，应说明系统会拒答或给出低置信度，不要现场承诺一定回答正确。

### DeepSeek API 暂时不可用

说明检索链路与生成链路是分开的：可以展示已有文档、接口文档、索引文件、日志和评估脚本，并如实说明外部 API 当前不可用。

### Docker 启动失败

回到本地开发启动方式完成主演示，再根据错误检查 Docker Desktop、端口、镜像构建和 `.env` 注入。不要声称 Docker 已验证通过。
