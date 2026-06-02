# RAG-study 项目演示流程

这份流程适合录制视频、课程答辩和面试展示。完整演示建议控制在 8 到 12 分钟。

---

## 1. 演示前准备

### 1.1 检查后端配置

确认项目根目录下已经有本地 `.env` 文件，并且已经填写自己的 DeepSeek API Key。不要在录屏或投屏时展示真实 API Key。

后端示例配置参考 `.env.example`：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

### 1.2 准备临时演示文档

在知识库目录之外准备一个 UTF-8 编码的文件：

```text
database_transaction_demo.txt
```

建议内容：

```text
数据库事务通常具有 ACID 四个特性。

Atomicity 表示原子性，一个事务中的操作要么全部成功，要么全部失败。
Consistency 表示一致性，事务执行前后数据库需要保持有效状态。
Isolation 表示隔离性，并发事务之间不应该互相干扰。
Durability 表示持久性，事务提交后的结果应该被永久保存。
```

这个文件只用于演示上传、索引重建、提问和删除流程。

### 1.3 启动后端

在项目根目录 `D:\Projects\RAG-study` 打开 PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

后端地址：

```text
http://127.0.0.1:8000
```

可以先检查：

```text
http://127.0.0.1:8000/health
```

预期结果：

```json
{
  "status": "ok",
  "service": "rag-api"
}
```

### 1.4 启动前端

打开另一个 PowerShell 终端：

```powershell
cd frontend
npm run dev
```

### 1.5 打开页面

浏览器访问：

```text
http://localhost:5173
```

进入页面后，确认可以看到：

* 上传知识库文档区域
* 当前知识库文档列表
* 问题输入框
* 提交问题按钮

---

## 2. 演示主流程

### 步骤 1：展示当前知识库文档列表

进入页面后，先展示“当前知识库文档”区域。

可以说明：

> 前端页面加载后会调用 `GET /documents`，读取本地知识库目录中的 `.txt` 文件。页面也提供手动刷新按钮。

当前默认示例文档包括：

```text
ai_tools_intro.txt
frontend_vue.txt
python_backend.txt
rag_intro.txt
```

### 步骤 2：提问已有知识库问题

在输入框中输入：

```text
开发 Python 后端 API 接口服务推荐用什么框架？
```

点击“提交问题”。

### 步骤 3：展示 answer 和 sources

回答出现后，重点展示：

* `answer`：模型根据检索资料生成的回答
* `sources`：引用来源列表
* 来源文件名
* `chunk_index`
* 相似度分数
* 可展开查看的原始片段内容

可以说明：

> 系统不是直接让模型自由回答，而是先检索知识库，再把检索到的 chunks 作为 context 交给模型。页面会展示引用来源，方便核对答案依据。

### 步骤 4：上传新的 txt 文档

在上传区域选择提前准备好的：

```text
database_transaction_demo.txt
```

点击“上传文档”。

上传成功后，页面会显示类似提示：

```text
文档上传成功，知识库索引已重建，当前 chunk 数量：...
```

### 步骤 5：展示上传后列表自动刷新

上传成功后，不要点击手动刷新按钮。

直接展示文档列表中已经出现：

```text
database_transaction_demo.txt
```

可以说明：

> 上传接口保存文件后，会重新读取全部知识库文档并重建 FAISS 索引。前端收到成功响应后，会自动再次调用 `GET /documents` 刷新列表。

### 步骤 6：提问新文档相关问题

输入：

```text
数据库事务的 ACID 是什么？
```

点击“提交问题”。

确认回答中说明了：

* Atomicity：原子性
* Consistency：一致性
* Isolation：隔离性
* Durability：持久性

展开引用来源，确认来源包含：

```text
database_transaction_demo.txt
```

### 步骤 7：删除测试文档

在文档列表中找到：

```text
database_transaction_demo.txt
```

点击“删除”。

浏览器会弹出二次确认框。确认删除后，观察对应按钮显示“删除中...”并处于禁用状态。

可以说明：

> 删除过程中禁用对应按钮，可以避免用户重复提交同一个删除请求。

### 步骤 8：展示删除后列表自动刷新

删除成功后，页面会显示类似提示：

```text
文档删除成功，知识库索引已重建，当前 chunk 数量：...
```

列表中的 `database_transaction_demo.txt` 会自动消失。

可以说明：

> 删除接口移除文件后也会重建 FAISS 索引，避免系统继续检索已经删除的内容。删除成功后，前端会自动刷新列表。

### 步骤 9：再次提问删除文档相关问题

再次输入：

```text
数据库事务的 ACID 是什么？
```

确认系统不能再根据已删除文档回答。

理想情况下，页面会显示：

```text
抱歉，我无法找到相关信息来回答您的问题。
```

并显示：

```text
暂无引用来源。
```

注意：最终结果取决于当前知识库是否还有其他包含 ACID 内容的文档。演示前应确认知识库中没有重复资料。

---

## 3. 推荐演示问题

### 默认知识库问题

```text
开发 Python 后端 API 接口服务推荐用什么框架？
```

预期来源：

```text
python_backend.txt
```

```text
AI 工具调用常用于哪些场景？
```

预期来源：

```text
ai_tools_intro.txt
```

### 上传测试文档后的问题

```text
数据库事务的 ACID 是什么？
```

预期来源：

```text
database_transaction_demo.txt
```

---

## 4. 演示时应该强调的技术点

### 4.1 RAG 流程

RAG 是检索增强生成。系统先检索知识库，再把检索结果作为 context 交给大模型，减少模型脱离资料自由发挥的情况。

### 4.2 chunk 切分

文档不会直接整篇交给模型，而是切分成多个 chunks。当前项目使用固定长度切分，并在相邻片段之间保留 overlap，降低上下文被截断的影响。

### 4.3 BGE embedding

项目使用 `BAAI/bge-small-zh-v1.5` 将知识库 chunks 和用户问题转换成向量，便于计算语义相似度。

### 4.4 FAISS 检索

FAISS 用于保存本地向量索引并检索最相似的 chunks。当前实现使用归一化向量和内积检索。

### 4.5 sources 引用来源

后端返回 `answer` 的同时返回 `sources`。前端会展示来源文件、`chunk_index`、相似度和原始片段，方便验证回答依据。

### 4.6 上传和删除后重建索引

文件内容变化后，原来的向量索引可能已经过期。因此，上传和删除成功后都需要重建索引，保证检索结果与当前知识库一致。

---

## 5. 常见演示故障排查

### 5.1 后端没有启动

**现象**

前端提交问题、加载文档列表或上传文件时提示请求失败。

**排查**

访问：

```text
http://127.0.0.1:8000/health
```

如果无法访问，在项目根目录重新启动：

```powershell
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

### 5.2 前端 API 地址配置错误

**现象**

后端已经启动，但前端仍然无法请求接口。

**排查**

检查 `frontend/.env.local`：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

修改环境变量后，需要重新运行：

```powershell
npm run dev
```

### 5.3 上传文件不是 UTF-8 编码

**现象**

上传时提示：

```text
文件编码必须是 UTF-8
```

**排查**

使用编辑器将测试 `.txt` 文件转换为 UTF-8 编码，再重新上传。

### 5.4 CORS 问题

**现象**

浏览器控制台出现跨域请求被拦截的错误。

**排查**

确认前端使用常见本地地址启动，例如：

```text
http://localhost:5173
http://127.0.0.1:5173
```

当前 FastAPI 后端已允许这些本地前端地址。如果使用了其他端口，需要同步调整后端 CORS 配置。

### 5.5 DeepSeek API Key 没有配置

**现象**

后端启动时报错：

```text
缺少 DEEPSEEK_API_KEY，请检查 .env 文件。
```

**排查**

参考 `.env.example` 创建本地 `.env` 文件，并填写自己的 API Key。录屏时不要展示真实 Key。

### 5.6 首次启动较慢

**现象**

启动 FastAPI 后没有立刻完成初始化。

**原因**

后端启动时会加载 BGE 模型、读取知识库并建立 FAISS 索引。首次加载模型可能需要更多时间。

### 5.7 删除演示文档后无法重建索引

**现象**

删除接口返回索引重建失败。

**排查**

确认知识库中至少还保留一个有效的 UTF-8 `.txt` 文档。当前实现要求至少加载到一个 chunk 才能建立索引。
