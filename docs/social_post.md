# RAG-study 社交平台展示文案

## 一、统一简短介绍

我用 FastAPI + Vue + DeepSeek API + BGE + FAISS 做了一个本地知识库 RAG 问答系统，支持上传资料、基于资料回答、显示引用来源、展示检索质量，还做了日志、评估脚本、索引持久化和 Docker 后端容器化。

## 二、抖音短文案

大二学生从零做了一个本地知识库 RAG 项目。

不是把问题直接丢给大模型，而是先用 BGE + FAISS 从本地资料里检索，再让 DeepSeek 基于资料回答。前端能看答案、引用来源和检索质量，也支持上传、删除 `.txt` 文档。

后面我又补了日志、评估脚本、索引持久化、manifest 检测和 Docker 后端容器化。项目不算生产级，但完整走通了一次 RAG 应用开发流程。

后续继续分享切片、检索、评估和踩坑过程，小白也能跟着理解。

## 三、小红书图文标题

1. 大二学生做完第一个 RAG 项目：从检索到前后端完整跑通
2. FastAPI + Vue + BGE + FAISS，本地知识库问答实战复盘
3. 不只会调 API：我给 RAG 项目补了引用、评估和索引持久化
4. 小白也能看懂的 RAG 项目结构：先检索，再回答
5. 17 天做一个本地知识库 RAG，我真正学到了什么

## 四、小红书正文

最近把自己的 `RAG-study` 项目整理到了可以完整演示的阶段。

它是一个本地知识库问答系统，技术栈是：

- FastAPI：后端接口
- Vue 3：前端页面
- BGE：文本 embedding
- FAISS：本地向量检索
- DeepSeek API：基于检索资料生成回答

基本流程可以理解成：

```text
本地 txt 资料
→ 切成 chunks
→ BGE 转成向量
→ FAISS 检索相关片段
→ DeepSeek 根据片段回答
→ 页面展示答案、引用来源和检索质量
```

除了基础问答，我还做了：

- 上传和删除 UTF-8 `.txt` 文档
- 上传/删除后自动重建索引
- 前端文档列表自动刷新
- `sources` 引用来源展示
- `retrieval_info` 检索质量展示
- JSONL 问答日志
- API 与基础评估脚本
- FAISS 索引持久化
- manifest 知识库变更检测
- Docker 后端容器化初步实现

这个项目目前不支持 PDF/Word，也没有鉴权、增量索引和完整线上部署。我更愿意把它当成一次完整的学习实战：不只让功能跑起来，还尝试处理可解释性、测试、索引一致性和部署准备。

后面会继续把切片、embedding、FAISS、拒答逻辑和评估方法拆开讲。想一起学习 AI 应用开发的，可以关注后续内容或进群交流，先看项目和资料是否适合自己。

## 五、粉丝群发布文案

今天把 `RAG-study` 的最终演示和项目文档整理完了。

这是一个 FastAPI + Vue + DeepSeek API + BGE + FAISS 的本地知识库 RAG 项目，已经走通：文档切片、向量检索、基于资料回答、引用来源、检索质量、文档上传删除、日志评估、索引持久化、manifest 检测和 Docker 后端容器化。

目前只支持 UTF-8 `.txt`，定位是学习和复现，不是直接商用的成品。群里后续会继续拆解项目结构、运行步骤和常见报错。大家可以先按 README 跑一遍，有具体错误时把命令和完整报错发出来，更容易定位。

## 六、GitHub 项目介绍文案

`RAG-study` is a local knowledge base RAG application built with FastAPI, Vue 3, DeepSeek API, `BAAI/bge-small-zh-v1.5`, and FAISS.

It supports context-based Q&A, source references, retrieval quality information, UTF-8 `.txt` document upload and deletion, request logs, evaluation scripts, FAISS index persistence, manifest-based knowledge base change detection, and initial backend containerization with Docker.

The project is designed for learning and local demonstration. It currently supports `.txt` files only and is not a production-ready SaaS application.

## 七、评论区回复模板

### RAG 是不是就是调教大模型？

不完全是。这个项目没有训练或微调大模型，主要是先从外部知识库检索资料，再把资料作为上下文交给模型回答。重点在检索、上下文组织和结果验证。

### 有没有切片？

有。文档会先切成 chunks，再分别生成 embedding。当前使用固定长度加 overlap 的基础方案，后续可以继续做按段落或语义切片。

### 用的什么向量模型？

用的是 `BAAI/bge-small-zh-v1.5`，主要考虑中文检索效果、本地运行和学习成本。

### 这个模型检索效果怎么样？

在当前小规模中文示例知识库里可以完成基础语义检索，但效果会受资料内容、切片、问题表达和阈值影响。我做了 `retrieval_info` 和评估问题集来观察结果，不会只凭一次回答判断模型好坏。

### 接入 RAG 后还会不会有误差？

会。RAG 能让回答更多基于指定资料，但检索可能漏召回，模型也可能理解或组织错误。项目通过阈值、拒答、引用来源和检索质量降低风险，但不能保证百分之百准确。

### FastAPI 是什么？

FastAPI 是 Python 的 Web API 框架。这个项目用它接收问题、返回答案，并提供文档列表、上传、删除和健康检查接口，还能自动生成接口文档。

### 这个项目能不能商用？

当前版本更适合学习和本地演示，不能直接当商用品。商用前还需要补鉴权、权限隔离、安全审计、限流、监控、数据合规、备份和更完整的测试部署。

### 后续会不会支持 PDF/Word？

有这个优化方向，但当前版本只支持 UTF-8 `.txt`。PDF/Word 还需要增加解析、清洗、表格和版面处理，不能只改一个文件扩展名。

## 八、面对质疑的回复模板

### “这不就是套 API 吗？”

DeepSeek API 是生成环节的一部分，但项目还包含文档切片、BGE embedding、FAISS 检索、阈值过滤、来源追踪、文档管理、日志评估、索引持久化和 manifest 检测。我的目标不是证明技术有多复杂，而是完整理解并实现一条 RAG 工程链路。

### “这也不算真正的知识库系统吧？”

如果按生产系统标准，它确实还不完整，所以我明确把它定位为本地学习项目。目前完成的是核心 RAG、文档管理和基础工程能力，鉴权、多租户、增量索引和监控仍是后续工作。

### “RAG 也会胡说，做了有什么用？”

RAG 不能彻底消除误差，但可以让回答有指定资料作为依据，并通过引用来源帮助人工核对。项目也保留了拒答和检索质量信息，重点是让错误更容易发现，而不是承诺绝对正确。

### “为什么不用现成框架？”

学习阶段我希望先理解文档切片、embedding、检索、阈值和上下文拼接的具体过程，所以保留了较清晰的自建模块。后续做更复杂应用时，再评估 LangChain、LlamaIndex 或其他框架是否能降低维护成本。

### “项目是不是已经上线了？”

没有。当前完成的是本地运行和 Docker 后端容器化初步实现，没有对外声称已经正式上线，也没有把它描述成完整 SaaS。
