# RAG-study 简历项目描述

## 一、简历一行版

独立开发基于 FastAPI、Vue、BGE、FAISS 和 DeepSeek API 的本地知识库 RAG 问答系统，实现文档管理、引用溯源、检索质量展示、日志评估、索引持久化及 Docker 后端容器化。

## 二、简历项目经历版

### 项目名称

RAG-study 本地知识库问答系统

### 技术栈

Python、FastAPI、Vue 3、Vite、DeepSeek API、BAAI/bge-small-zh-v1.5、FAISS、Docker

### 项目描述

面向本地学习资料构建的 RAG 问答系统。系统先从本地知识库检索相关文本片段，再调用 DeepSeek API 基于检索上下文生成回答，并在前端展示引用来源和检索质量。

### 职责/工作内容

- 独立完成 DeepSeek API 封装、环境变量管理、异常处理和重试机制。
- 实现 UTF-8 `.txt` 文档读取、固定长度 chunk 切分和来源元数据保留。
- 使用 BGE 生成文本 embedding，使用 FAISS 构建和查询本地向量索引。
- 使用 FastAPI 提供问答、健康检查、文档列表、上传和删除接口。
- 使用 Vue 3 实现问答、`sources`、`retrieval_info` 和文档管理页面。
- 实现上传/删除后索引重建及前端文档列表自动刷新。

### 项目亮点

- 返回 `sources`，展示来源文件、`chunk_index`、相似度和原始片段，提高回答可追踪性。
- 返回 `retrieval_info`，展示命中状态、最高分、来源数量和置信度，便于分析检索质量。
- 对低相关检索结果进行阈值过滤，知识库无相关资料时拒答或给出低置信度。

### 工程优化

- 增加 JSONL 问答日志，记录问题、回答和检索信息。
- 持久化 FAISS 索引与 chunks，后端重启时优先加载已有索引。
- 使用 manifest 检测知识库变化，变化时自动重建索引，保证文件与索引一致。
- 使用 Dockerfile 和 docker-compose 完成后端容器化初步实现。

### 测试与评估

- 编写接口测试、评估问题集、索引持久化测试和 manifest 一致性测试脚本。
- 覆盖已知问题命中、未知问题拒答、索引加载和知识库变化重建等场景。

### 后续优化方向

支持 PDF/Word、语义切片、增量索引、混合检索、rerank、鉴权和更完整的自动评估。目前项目定位为本地学习系统，不是完整 SaaS。

## 三、STAR 法描述版

### S（Situation，背景）

通用大模型不能直接了解用户本地资料，而且仅看最终回答很难判断答案依据和检索效果。

### T（Task，任务）

独立实现一个可在本地运行的知识库 RAG 问答系统，覆盖资料读取、向量检索、模型生成、前端展示、文档管理和基础部署流程。

### A（Action，行动）

- 使用 BGE 将文档 chunks 和用户问题转换为 embedding，通过 FAISS 完成语义检索。
- 使用 FastAPI 封装 `/ask`、`/documents`、上传和删除等接口，调用 DeepSeek API 生成回答。
- 使用 Vue 3 展示答案、引用来源、检索质量及文档列表。
- 增加日志和评估脚本，定位检索与生成问题。
- 增加 FAISS 索引持久化和 manifest 检测，优化重启速度并保证索引一致性。
- 使用 Dockerfile 和 docker-compose 完成后端容器化初步实现。

### R（Result，结果）

完成了一个可本地演示的 RAG 应用闭环：能够上传和删除 UTF-8 `.txt` 资料、基于资料回答、展示引用和检索信息，并通过脚本验证接口、持久化和知识库变更场景。项目仍需扩展文档格式、增量更新和生产安全能力。

## 四、技术亮点版

- **RAG 检索生成**：BGE embedding + FAISS + DeepSeek API。
- **接口设计**：FastAPI + Pydantic，覆盖问答与文档管理。
- **前端交互**：Vue 3 + Vite，包含加载、错误、上传、删除和自动刷新状态。
- **可解释性**：`sources` 引用来源与 `retrieval_info` 检索质量。
- **一致性**：索引持久化 + manifest 变更检测。
- **可测试性**：问答日志、API 测试、评估问题集和索引专项测试。
- **部署准备**：Docker 后端容器化初步实现。

## 五、面试追问回答版

### 你独立完成了哪些部分？

我从 DeepSeek API 封装开始，依次完成了文档读取与切片、BGE embedding、FAISS 检索、RAGService、FastAPI 接口、Vue 页面、文档上传删除、日志评估、索引持久化、manifest 检测和 Docker 后端容器化。

### 为什么使用 BGE 和 FAISS？

BGE 对中文语义检索比较适合，`bge-small-zh-v1.5` 的体积也适合本地学习项目。FAISS 不需要额外部署数据库服务，便于理解和实现向量索引的核心流程。

### 怎么判断回答是否可信？

项目会展示 `sources` 和原始片段，用户可以核对答案依据；`retrieval_info` 还能展示检索分数和置信度。不过这不能完全消除模型误差，所以我不会承诺回答百分之百正确。

### 索引持久化解决了什么问题？

它避免后端每次重启都重新计算全部文档 embedding。服务可以优先加载已有的 FAISS 索引和 chunks，提高重复启动效率。

### manifest 有什么作用？

只加载旧索引可能导致索引和知识库文件不一致。manifest 记录知识库文件状态，启动时进行比较；发生变化就重新构建索引。

### 项目目前最大的不足是什么？

目前只支持 UTF-8 `.txt`，文档变化后仍全量重建，也没有鉴权、增量更新、混合检索和生产监控。因此它是本地学习项目，不是完整 SaaS。

## 六、中文版

**RAG-study 本地知识库问答系统**  
技术栈：Python、FastAPI、Vue 3、Vite、DeepSeek API、BGE、FAISS、Docker

- 独立完成本地知识库 RAG 系统，覆盖 API 封装、文本切片、向量检索、模型生成、前端交互和文档管理。
- 使用 `BAAI/bge-small-zh-v1.5` 生成 embedding，使用 FAISS 检索相关 chunks，并调用 DeepSeek API 基于上下文生成回答。
- 使用 FastAPI 提供问答、文档列表、上传和删除接口，使用 Vue 3 展示答案、引用来源和检索质量。
- 增加 JSONL 日志、基础评估脚本、索引持久化和 manifest 变更检测，提高可解释性、可测试性和索引一致性。
- 使用 Dockerfile 和 docker-compose 完成后端容器化初步实现；当前仅支持 UTF-8 `.txt`，定位为本地学习项目。

## 七、英文版

**RAG-study: Local Knowledge Base RAG System**  
Tech Stack: Python, FastAPI, Vue 3, Vite, DeepSeek API, BGE, FAISS, Docker

- Independently built a local RAG application covering API integration, text chunking, vector retrieval, answer generation, frontend interaction, and document management.
- Used `BAAI/bge-small-zh-v1.5` to generate embeddings and FAISS to retrieve relevant text chunks, then called the DeepSeek API to generate context-based answers.
- Built FastAPI endpoints for Q&A, document listing, upload, and deletion, and developed a Vue 3 interface for answers, sources, retrieval quality, and document operations.
- Added JSONL logs, evaluation scripts, FAISS index persistence, and manifest-based change detection to improve explainability, testing, startup efficiency, and index consistency.
- Added initial backend containerization with Dockerfile and docker-compose. The current version supports UTF-8 `.txt` files and is designed as a local learning project rather than a complete SaaS product.
