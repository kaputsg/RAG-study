# RAG-study GitHub / 作品集展示说明

这份文档用于整理 RAG-study 在 GitHub、个人作品集、简历和社交平台中的展示方式。表达重点是“完整 AI 应用开发流程”和“本地知识库 RAG 原型”，不要把项目包装成正式商用产品。

---

## 1. GitHub 项目首页应该重点展示什么

GitHub 首页应该让访问者快速看懂四件事：

1. 项目是什么：基于 FastAPI、Vue、BGE、FAISS 和 DeepSeek API 的本地知识库 RAG 问答系统。
2. 它不是简单调 API：包含文档读取、chunk 切分、embedding、FAISS 检索、上下文拼接、模型生成和来源展示。
3. 已实现哪些能力：问答、sources、retrieval_info、文档上传、文档列表、删除、日志、评估、索引持久化、manifest 检测和后端 Docker 化。
4. 当前边界：只支持 UTF-8 `.txt`，定位是本地学习和演示项目，不是已经上线的产品。

---

## 2. README 首屏建议

README 首屏建议包含：

- 一句话说明项目：本地知识库 RAG 问答系统。
- 核心技术栈：FastAPI、Vue 3、BGE、FAISS、DeepSeek API、Docker。
- 主要功能：问答、引用来源、检索信息、文档管理、日志评估、索引持久化。
- 当前限制：仅支持 UTF-8 `.txt` 文档。
- 快速启动入口：后端启动、前端启动、Docker 后端启动。
- 演示与面试资料入口：方便 HR、老师或面试官快速查看。

README 不建议写得像产品官网，应该清楚、直接、可验证。

---

## 3. 项目截图建议

建议准备 4 类截图，但本次任务不创建图片：

1. 问答页面：展示输入问题、answer 和 sources。
2. retrieval_info 区域：展示命中状态、相似度、来源数量或置信度。
3. 文档管理区域：展示上传、文档列表和删除按钮。
4. 后端接口文档：展示 FastAPI `/docs` 中的接口列表。

截图说明要真实，不要写“支持所有文档格式”。可以写“当前演示使用 UTF-8 txt 文档”。

---

## 4. 演示视频建议

演示视频建议控制在 2 到 4 分钟：

1. 先展示项目目录和 README，说明技术栈。
2. 启动 FastAPI 后端和 Vue 前端。
3. 打开前端，展示当前文档列表。
4. 提一个知识库内问题，展示 answer、sources 和 retrieval_info。
5. 提一个知识库外问题，展示拒答或低置信度效果。
6. 上传一个 txt 文档，说明上传后会重建索引并刷新列表。
7. 删除文档，说明删除后也会重建索引。
8. 简单展示 Docker 后端启动文档，但不要声称项目已经上线。

---

## 5. 作品集页面介绍文案

RAG-study 是一个本地知识库 RAG 问答项目，使用 FastAPI、Vue 3、BGE、FAISS 和 DeepSeek API 实现。项目围绕“先检索资料，再生成回答”的流程构建，支持 UTF-8 `.txt` 文档上传、列表展示和删除，能够返回答案、引用来源和检索质量信息。

这个项目重点展示了我对 AI 应用开发完整链路的实践：API 调用、环境变量管理、文档加载、chunk 切分、embedding、向量检索、后端接口、前端交互、日志评估、索引持久化、manifest 变更检测和 Docker 后端容器化。

当前项目定位为本地学习和作品集展示，不是正式上线产品。

---

## 6. 项目亮点 bullet points

- 不是简单调用大模型 API，而是实现了 RAG 检索链路。
- 使用 BGE 中文 embedding 和 FAISS 本地向量检索。
- 使用 FastAPI 提供问答、健康检查、文档列表、上传和删除接口。
- 使用 Vue 3 实现问答页面、sources 展示、retrieval_info 展示和文档管理。
- 上传和删除 txt 文档后自动重建索引，保持知识库和索引一致。
- 返回 sources，方便核对回答引用来源。
- 返回 retrieval_info，辅助判断检索质量。
- 增加 JSONL 问答日志和基础评估问题集。
- 支持 FAISS 索引持久化，减少重复启动时的索引构建成本。
- 使用 manifest 检测知识库变更，避免加载过期索引。
- 完成 Docker 后端容器化初步实现。
- 当前只支持 UTF-8 `.txt`，没有包装成万能知识库。

---

## 7. 项目目录怎么讲

可以这样介绍项目目录：

- `app/`：后端核心代码，包括 FastAPI 接口、配置、DeepSeek API 客户端、文档加载、RAGService 和向量检索。
- `frontend/`：Vue 3 前端页面，负责问答交互、sources/retrieval_info 展示和文档管理。
- `data/knowledge_base/`：本地 txt 知识库目录。
- `scripts/`：接口测试、评估、索引持久化和 manifest 相关脚本。
- `docs/`：部署、Docker、演示、面试和作品集文档。
- `Dockerfile`、`docker-compose.yml`：后端 Docker 化初步实现。

讲目录时不要只说“结构清晰”，要对应到每个目录承担的功能。

---

## 8. 给 HR 看的版本

RAG-study 是我独立完成的本地知识库 AI 问答项目。项目从后端 API、前端页面、知识库检索、文档管理、日志评估到 Docker 后端容器化都有实践，体现了我对 AI 应用开发完整流程的学习和动手能力。

技术栈包括 FastAPI、Vue 3、BGE、FAISS 和 DeepSeek API。项目目前适合本地演示和作品集展示，已实现 txt 文档上传、删除、问答、引用来源展示和检索信息展示。

---

## 9. 给技术面试官看的版本

RAG-study 的核心链路是：文档加载和 chunk 切分 -> BGE embedding -> FAISS 向量索引 -> 问题向量化 -> Top K 检索与阈值过滤 -> context 拼接 -> DeepSeek API 生成 -> answer/sources/retrieval_info 返回。

工程上，项目使用 FastAPI 封装接口，Vue 3 做前端交互，支持文档上传、删除和列表刷新；通过 JSONL 日志和评估脚本观察问答质量；通过 FAISS 索引持久化和 manifest 变更检测减少重复构建并保证索引一致性；通过 Dockerfile 和 docker-compose 做后端容器化初步实践。

当前边界是：只支持 UTF-8 `.txt`，没有权限系统、数据库后台、增量索引和正式部署链路。

---

## 10. 给同学/粉丝看的版本

我做了一个本地知识库 AI 问答项目：把自己的 txt 资料放进去，然后可以围绕这些资料提问。系统会先查资料，再让大模型回答，还会告诉你答案参考了哪份文件、哪一段内容。

这个项目让我从“会调用 API”往前走了一步，实践了后端接口、前端页面、向量检索、RAG、日志评估、索引持久化和 Docker。它现在还不是一个万能知识库，只支持 txt，但已经能完整展示一个 AI 应用从想法到可演示原型的过程。
