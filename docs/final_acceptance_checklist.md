# RAG-study 项目最终验收清单

> 使用方法：验收时逐项实际操作并勾选。涉及真实 API Key、日志内容或本地路径时，录屏前注意脱敏。

## 一、本地开发环境验收

- [ ] 后端本地启动成功
- [ ] 前端本地启动成功
- [ ] `http://127.0.0.1:8000/health` 正常
- [ ] `http://127.0.0.1:8000/docs` 正常
- [ ] `http://localhost:5173` 正常打开

## 二、RAG 问答功能验收

- [ ] `POST /ask` 能返回 `answer`
- [ ] `POST /ask` 能返回 `sources`
- [ ] `POST /ask` 能返回 `retrieval_info`
- [ ] 已知问题能命中知识库
- [ ] 未知问题能拒答或显示低置信度
- [ ] `sources` 能展示 `source`、`chunk_index`、`score`
- [ ] `retrieval_info` 能展示 `hit`、`max_score`、`source_count`、`confidence`

## 三、知识库文档管理验收

- [ ] `GET /documents` 能返回文档列表
- [ ] 前端能展示知识库文档列表
- [ ] 上传 UTF-8 `.txt` 文档成功
- [ ] 上传后自动重建索引
- [ ] 上传后前端文档列表自动刷新
- [ ] 删除文档前有二次确认
- [ ] 删除文档成功
- [ ] 删除后自动重建索引
- [ ] 删除后前端文档列表自动刷新

## 四、索引与一致性验收

- [ ] `data/vector_store/faiss.index` 运行时生成
- [ ] `data/vector_store/chunks.json` 运行时生成
- [ ] `data/vector_store/manifest.json` 运行时生成
- [ ] 索引文件不会提交到 Git
- [ ] 后端再次启动时优先加载已有索引
- [ ] 知识库文件变化后 manifest 能触发重建索引

## 五、日志与评估验收

- [ ] `logs/rag_requests.jsonl` 能写入问答日志
- [ ] 日志不会提交到 Git
- [ ] `python -m scripts.day13_test_api` 能运行
- [ ] `python -m scripts.day13_eval_questions` 能运行
- [ ] `python -m scripts.day14_test_persist_index` 能运行
- [ ] `python -m scripts.day15_test_index_manifest` 能运行

## 六、Docker 验收

- [ ] `docker build -t rag-study-backend .` 成功
- [ ] `docker run --env-file .env -p 8000:8000 rag-study-backend` 成功
- [ ] `docker compose up --build` 成功
- [ ] Docker 后端 `/health` 正常
- [ ] Docker 后端 `/docs` 正常
- [ ] 前端本地可以连接 Docker 后端

## 七、Git 与安全验收

- [ ] `.env` 未提交
- [ ] `frontend/.env.local` 未提交
- [ ] `logs/rag_requests.jsonl` 未提交
- [ ] `data/vector_store/*.index` 未提交
- [ ] `data/vector_store/*.json` 未提交
- [ ] `frontend/node_modules` 未提交
- [ ] `frontend/dist` 未提交
- [ ] `AGENTS.md` 未提交
- [ ] `git status` 检查通过

## 八、文档验收

- [ ] `README.md` 可读
- [ ] `docs/demo_flow.md` 可读
- [ ] `docs/interview_qa.md` 可读
- [ ] `docs/deployment_guide.md` 可读
- [ ] `docs/docker_guide.md` 可读
- [ ] `docs/final_acceptance_checklist.md` 可读
- [ ] `docs/final_demo_script.md` 可读
- [ ] `docs/project_pitch.md` 可读
- [ ] `docs/resume_project.md` 可读
- [ ] `docs/social_post.md` 可读

## 验收记录

- 验收日期：
- 验收环境：
- 验收人：
- 未通过项及原因：
- 修复后复测结果：
