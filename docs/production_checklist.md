# RAG-study 上线前安全检查清单

## 一、敏感信息检查

* [ ] `.env` 未提交
* [ ] DeepSeek API Key 未写入 README/docs
* [ ] `frontend/.env.local` 未提交
* [ ] 真实 token、密码、密钥没有出现在代码仓库

## 二、运行时文件检查

* [ ] `logs/rag_requests.jsonl` 未提交
* [ ] `data/vector_store/faiss.index` 未提交
* [ ] `data/vector_store/chunks.json` 未提交
* [ ] `data/vector_store/manifest.json` 未提交
* [ ] `frontend/node_modules` 未提交
* [ ] `frontend/dist` 未提交
* [ ] Python 虚拟环境未提交

## 三、接口安全检查

* [ ] 上传接口只允许 `.txt`
* [ ] 上传接口检查 UTF-8
* [ ] 上传接口使用安全文件名，避免路径穿越
* [ ] 删除接口使用安全文件名，避免路径穿越
* [ ] 删除文档前前端有二次确认
* [ ] CORS 生产环境不建议使用 `allow_origins=["*"]`

## 四、部署配置检查

* [ ] 后端 `.env` 已配置
* [ ] 前端 `VITE_API_BASE_URL` 指向正确后端地址
* [ ] 前端 `npm run build` 通过
* [ ] 后端启动命令不使用 `--reload`
* [ ] 后端监听地址按部署环境设置
* [ ] 后端接口 `/health` 正常

## 五、RAG 功能检查

* [ ] `/ask` 正常返回 `answer`、`sources`、`retrieval_info`
* [ ] 上传文档后能重建索引
* [ ] 删除文档后能重建索引
* [ ] 知识库变更后 `manifest` 能触发自动重建
* [ ] RAG 日志正常写入
* [ ] eval 脚本能运行

## 六、上线前最后检查

* [ ] `git status` 干净
* [ ] 没有误提交 `AGENTS.md`
* [ ] README 启动命令可用
* [ ] `docs/deployment_guide.md` 可读
* [ ] `docs/production_checklist.md` 可读
