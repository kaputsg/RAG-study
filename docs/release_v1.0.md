# RAG-study v1.0 版本说明

## 1. 版本信息

- 版本号：v1.0
- 项目阶段：第一阶段完成
- 项目定位：本地知识库 RAG 问答系统
- 当前状态：可本地运行、可演示、可写入简历、可用于学习复盘

RAG-study 是一个基于 FastAPI、Vue、BGE、FAISS 和 DeepSeek API 的本地知识库 RAG 问答项目。v1.0 的目标不是做成完整产品，而是完成一个结构清楚、可以运行、可以演示、适合学习复盘的 AI 应用原型。

## 2. v1.0 完成范围

v1.0 已完成以下范围：

- DeepSeek API 调用
- BGE Embedding
- FAISS 检索
- FastAPI 后端
- Vue 前端
- txt 知识库
- chunk 切分
- 文档上传/删除
- sources 引用来源
- retrieval_info 检索质量
- 问答日志
- 评估脚本
- 索引持久化
- manifest 变更检测
- Docker 后端容器化
- README 和 docs 文档体系

## 3. 核心功能

- 基于本地 `.txt` 文档构建知识库。
- 将文档切分为 chunks，并保留来源信息。
- 使用 `BAAI/bge-small-zh-v1.5` 生成中文文本向量。
- 使用 FAISS 建立本地向量索引并进行相似度检索。
- 将检索结果作为上下文传给 DeepSeek API 生成回答。
- 返回 `answer`、`sources` 和 `retrieval_info`。
- 支持文档列表、上传和删除。
- 上传或删除文档后自动重建索引。
- 记录基础问答日志，并提供评估脚本辅助检查效果。

## 4. 技术栈

后端：

- Python
- FastAPI
- Pydantic
- DeepSeek API
- sentence-transformers
- BGE 中文 Embedding 模型：`BAAI/bge-small-zh-v1.5`
- FAISS
- python-dotenv

前端：

- Vue 3
- Vite
- JavaScript
- Fetch API

工程与部署准备：

- `.env` 配置管理
- Dockerfile
- docker-compose
- README 和 docs 文档体系

## 5. 项目结构说明

```text
RAG-study/
├─ app/                    # FastAPI 后端、RAG 服务、向量检索、文档处理
├─ data/                   # 本地知识库数据
├─ docs/                   # 演示、部署、面试、复盘和版本说明文档
├─ frontend/               # Vue 前端页面
├─ scripts/                # 测试、评估和辅助脚本
├─ Dockerfile              # 后端容器镜像定义
├─ docker-compose.yml      # 本地后端容器启动配置
├─ requirements.txt        # Python 依赖
└─ README.md               # 项目说明入口
```

## 6. 后端接口说明

当前后端提供以下接口：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/` | 项目基础信息 |
| GET | `/health` | 健康检查 |
| POST | `/ask` | 提交问题并返回 RAG 回答 |
| GET | `/documents` | 获取当前知识库文档列表 |
| POST | `/documents/upload` | 上传 `.txt` 文档并重建索引 |
| DELETE | `/documents/{filename}` | 删除指定文档并重建索引 |

## 7. 前端功能说明

当前前端支持：

- 输入问题。
- 提交问答请求。
- 展示 `answer`。
- 展示 `sources` 引用来源。
- 展示 `retrieval_info` 检索质量信息。
- 上传 `.txt` 文档。
- 展示文档列表。
- 删除文档。
- 上传或删除成功后刷新文档列表。

## 8. RAG 检索链路

当前 RAG 链路如下：

```text
txt 文档
  -> 文档读取
  -> chunk 切分
  -> BGE 生成向量
  -> FAISS 建立索引
  -> 用户提问
  -> 问题向量化
  -> 相似度检索
  -> 相似度阈值过滤
  -> 构造上下文
  -> DeepSeek API 生成回答
  -> 返回 answer / sources / retrieval_info
```

这个链路让回答不只依赖模型本身，而是尽量基于本地知识库中的可追溯片段。

## 9. 工程化能力

v1.0 中已经包含一些基础工程化能力：

- 使用 `.env` 管理 DeepSeek API Key 等配置。
- 将 DeepSeek 调用、文档加载、向量检索和 RAG 流程拆分为独立模块。
- 后端使用 FastAPI 提供结构化接口。
- 前端通过 API 对接后端，并展示 loading、错误和结果状态。
- 上传和删除文档后自动重建知识库索引。
- 使用 FAISS 索引持久化减少重复构建成本。
- 使用 manifest 检测知识库变化，避免加载过期索引。
- 通过日志和评估脚本辅助观察 RAG 效果。

## 10. Docker 后端容器化

v1.0 已完成 FastAPI 后端的 Docker 容器化初步实现：

- 提供 `Dockerfile`。
- 提供 `docker-compose.yml`。
- 支持通过 `.env` 注入本地配置。
- 支持在本地 Docker 环境中启动后端服务。

当前 Docker 能力主要用于本地环境复现和部署准备，不表示项目已经正式上线。

## 11. 文档与演示材料

当前项目已经整理了以下材料：

- README 项目说明。
- 演示流程文档。
- 最终验收清单。
- 最终演示脚本。
- 项目讲解稿。
- 简历项目描述。
- 面试问答和追问训练。
- 技术亮点总结。
- 作品集展示说明。
- Day 1-Day 20 学习复盘和总结。
- 第二阶段规划。

这些文档用于项目展示、学习复盘、面试准备和后续迭代。

## 12. 当前限制

当前项目仍然是本地学习型 RAG 原型，主要限制包括：

- 目前只支持 txt 文档。
- 暂不支持 PDF / Word。
- 暂无用户登录和权限系统。
- 暂无数据库保存对话历史。
- 暂未正式上线服务器。
- RAG 不能 100% 消除模型幻觉。
- 检索效果受知识库质量、chunk 参数、向量模型、相似度阈值影响。

## 13. 后续优化方向

后续可以围绕以下方向继续扩展：

- 规划接入 PDF、Word、Markdown 等更多文档格式。
- 优化 chunk 策略，从固定长度切分逐步改为更接近语义结构的切分。
- 引入 rerank 重排序，提高检索片段质量。
- 支持流式输出，改善问答体验。
- 增加对话历史，让多轮问答更自然。
- 使用数据库保存问答记录和文档元信息。
- 优化前端 UI，使演示和日常使用更清楚。
- 完善云服务器部署、Nginx 和 HTTPS 配置。

## 14. 适合展示的项目亮点

- 从 0 到 1 完成了一个本地知识库 RAG 应用原型。
- 覆盖了文档处理、向量化、检索、生成、接口和前端展示的完整链路。
- 使用 `sources` 和 `retrieval_info` 展示回答依据和检索质量。
- 支持文档上传、删除和索引重建，具备基础知识库管理能力。
- 加入日志、评估脚本、索引持久化和 manifest 检测，体现工程化意识。
- 完成了 README、演示、面试、简历、验收和复盘文档，便于展示和继续迭代。

## 15. v1.0 验收标准

v1.0 的验收标准如下：

- 后端可以在本地启动。
- 前端可以在本地启动。
- 可以提交问题并获得基于知识库的回答。
- 回答结果包含 `answer`。
- 回答结果包含 `sources`。
- 回答结果包含 `retrieval_info`。
- 可以查看当前文档列表。
- 可以上传 `.txt` 文档。
- 可以删除 `.txt` 文档。
- 上传和删除后可以自动重建索引。
- FAISS 索引可以持久化。
- manifest 可以检测知识库变化。
- Docker 后端容器化可以作为本地部署准备。
- README 和 docs 文档体系完整，能够支撑演示、面试和学习复盘。
