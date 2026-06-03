<script setup>
import { ref, onMounted } from "vue"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"


// 用户输入的问题
const question = ref("")

// 后端返回的回答
const answer = ref("")

// 后端返回的引用来源
const sources = ref([])

// 后端返回的检索质量信息
const retrievalInfo = ref(null)

// 加载状态
const loading = ref(false)

// 错误信息
const errorMessage = ref("")

const selectedFile = ref(null)

const uploadMessage = ref("")

const uploading = ref(false)

const documents = ref([])

const documentsLoading = ref(false)

const documentsError = ref("")

const deletingFilename = ref("")

const documentMessage = ref("")

async function loadDocuments() {
  documentsLoading.value = true
  documentsError.value = ""

  try {
    const response = await fetch(`${API_BASE_URL}/documents`)

    if (!response.ok) {
      let message = "获取文档列表失败"
      try {
        const errorData = await response.json()
        message = errorData.detail || message
      } catch {
        message = `获取文档列表失败，状态码：${response.status}`
      }
      throw new Error(message)
    }

    const data = await response.json()
    documents.value = data.documents || []
  } catch (error) {
    console.error("获取文档列表失败：", error)
    documentsError.value = error.message
  } finally {
    documentsLoading.value = false
  }
}

async function deleteDocument(filename) {
  const confirmed = window.confirm(`确认删除文档：${filename}？`)

  if (!confirmed) {
    return
  }

  deletingFilename.value = filename
  documentMessage.value = ""
  documentsError.value = ""

  try {
    const response = await fetch(`${API_BASE_URL}/documents/${encodeURIComponent(filename)}`, {
      method: "DELETE"
    })

    if (!response.ok) {
      let message = "删除文档失败"

      try {
        const errorData = await response.json()
        message = errorData.detail || message
      } catch {
        message = `删除文档失败，状态码：${response.status}`
      }

      throw new Error(message)
    }

    const data = await response.json()

    documentMessage.value = `${data.message}，当前 chunk 数量：${data.chunk_count}`

    await loadDocuments()
  } catch (error) {
    console.error("删除文档失败：", error)
    documentsError.value = error.message
  } finally {
    deletingFilename.value = ""
  }
}

async function handleSubmit() {
  if (!question.value.trim()) {
  answer.value = "请先输入问题。"
  sources.value = []
  retrievalInfo.value = null
  errorMessage.value = ""
  return
  }

  loading.value = true
  answer.value = ""
  sources.value = []
  retrievalInfo.value = null
  errorMessage.value = ""

  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: question.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || "请求失败")
    }

    const data = await response.json()

    answer.value = data.answer
    sources.value = data.sources || []
    retrievalInfo.value = data.retrieval_info || null
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}

function handleFileChange(event) {
  selectedFile.value = event.target.files[0] || null
  uploadMessage.value = ""
}

async function handleUpload() {
  if (!selectedFile.value) {
    uploadMessage.value = "请先选择 txt 文件。"
    return
  }

  if (!selectedFile.value.name.toLowerCase().endsWith(".txt")) {
    uploadMessage.value = "目前只支持上传 .txt 文件。"
    return
  }

  uploading.value = true
  uploadMessage.value = ""
  errorMessage.value = ""

  try {
    const formData = new FormData()
    formData.append("file", selectedFile.value)

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: "POST",
      body: formData
    })

    if (!response.ok) {
      let errorMessage = `上传失败（HTTP ${response.status}）`

      try {
        const errorData = await response.json()
        errorMessage = errorData.detail || errorMessage
      } catch {
        // 后端未返回 JSON 时保留 HTTP 状态码，避免丢失错误信息。
      }

      throw new Error(errorMessage)
    }

    const data = await response.json()
    uploadMessage.value = `${data.message}，当前 chunk 数量：${data.chunk_count}`
    await loadDocuments()
  } catch (error) {
    console.error("上传失败：", error)
    uploadMessage.value = `上传失败：${error.message}`
  } finally {
    uploading.value = false
  }
}

onMounted(() => {
  loadDocuments()
})
</script>


<template>
  <main class="page">
    <section class="card">
      <h1>本地知识库 RAG 问答系统</h1>
      <p class="subtitle">输入问题，后续会调用 FastAPI 后端获取回答。</p>

      <div class="upload-box">
        <h2>上传知识库文档</h2>
        <p class="upload-tip">当前支持上传 UTF-8 编码的 .txt 文件。</p>

        <div class="upload-row">
          <input
            type="file"
            accept=".txt"
            @change="handleFileChange"
            :disabled="uploading"
          />

          <button
            class="upload-button"
            @click="handleUpload"
            :disabled="uploading"
          >
            {{ uploading ? "上传中..." : "上传文档" }}
          </button>
        </div>

        <p class="upload-message" v-if="uploadMessage">
          {{ uploadMessage }}
        </p>
      </div>

      <div class="documents-box">
        <div class="documents-header">
          <h2>当前知识库文档</h2>
          <button
            class="secondary-button"
            @click="loadDocuments"
            :disabled="documentsLoading"
          >
            {{ documentsLoading ? "刷新中..." : "刷新列表" }}
          </button>
        </div>

        <p class="documents-error" v-if="documentsError">
          {{ documentsError }}
        </p>

        <p class="documents-message" v-if="documentMessage">
          {{ documentMessage }}
        </p>

        <p
          class="documents-empty"
          v-if="!documentsLoading && documents.length === 0"
        >
          当前知识库暂无文档。
        </p>

        <div class="document-list" v-if="documents.length > 0">
          <div
            class="document-item"
            v-for="document in documents"
            :key="document.filename"
          >
            <div class="document-info">
              <strong>{{ document.filename }}</strong>
              <p>{{ document.path }}</p>
            </div>

            <div class="document-actions">
              <span>{{ document.size }} bytes</span>

              <button
                class="danger-button"
                @click="deleteDocument(document.filename)"
                :disabled="deletingFilename === document.filename"
              >
                {{ deletingFilename === document.filename ? "删除中..." : "删除" }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <textarea
        v-model="question"
        :disabled="loading"
        placeholder="例如：开发 Python 后端 API 接口服务推荐用什么框架？"
      ></textarea>

      <button @click="handleSubmit" :disabled="loading">
        {{ loading ? "正在思考..." : "提交问题" }}
      </button>

      <p class="loading-text" v-if="loading">
        正在检索知识库并生成回答，请稍等...
      </p>

      <div class="error-box" v-if="errorMessage">
        {{ errorMessage }}
      </div>

      <div class="answer-box" v-if="answer">
        <h2>回答</h2>
        <p>{{ answer }}</p>
      </div>

      <div class="retrieval-box" v-if="retrievalInfo">
        <h2>检索质量</h2>
        <div class="retrieval-grid">
          <div>
            <span>是否命中知识库</span>
            <strong>{{ retrievalInfo.hit ? "是" : "否" }}</strong>
          </div>
          <div>
            <span>最高相似度</span>
            <strong>{{ Number(retrievalInfo.max_score || 0).toFixed(4) }}</strong>
          </div>
          <div>
            <span>引用来源数量</span>
            <strong>{{ retrievalInfo.source_count }}</strong>
          </div>
          <div>
            <span>置信度</span>
            <strong>{{ retrievalInfo.confidence }}</strong>
          </div>
        </div>
      </div>

       <p class="no-sources" v-if="answer && sources.length === 0">
          暂无引用来源。
       </p>

      <div class="sources-box" v-if="sources.length > 0">
        <h2>引用来源</h2>

        <div
          class="source-item"
          v-for="(source, index) in sources"
          :key="index"
        >
          <div class="source-meta">
            <span>文件：{{ source.source }}</span>
            <span>片段：{{ source.chunk_index }}</span>
            <span>相似度：{{ source.score.toFixed(4) }}</span>
          </div>

          <details class="source-detail">
            <summary>查看片段内容</summary>
            <p class="source-text">{{ source.text }}</p>
          </details>
        </div>
      </div>

    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fb;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 60px 20px;
}

.card {
  width: 100%;
  max-width: 760px;
  background: white;
  border-radius: 18px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

h1 {
  margin: 0;
  font-size: 28px;
}

.subtitle {
  color: #666;
  margin-top: 10px;
  margin-bottom: 24px;
}

.upload-box {
  margin-bottom: 28px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: #f9fafb;
}

.upload-box h2 {
  margin-top: 0;
  font-size: 20px;
}

.upload-tip {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 14px;
}

.upload-row {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.upload-row input {
  flex: 1;
}

.upload-button {
  margin-top: 0;
}

.upload-message {
  margin-top: 14px;
  color: #374151;
  font-size: 14px;
}

.documents-box {
  margin-bottom: 28px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: #f9fafb;
}

.documents-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.documents-header h2 {
  margin: 0;
  font-size: 20px;
}

.secondary-button {
  margin-top: 0;
  padding: 9px 14px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  font-size: 14px;
}

.secondary-button:hover {
  background: #f3f4f6;
}

.documents-error {
  margin: 16px 0 0;
  color: #b91c1c;
  font-size: 14px;
}

.documents-message {
  color: #065f46;
  background: #d1fae5;
  padding: 10px;
  border-radius: 10px;
  font-size: 14px;
}

.documents-empty {
  margin: 16px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.document-list {
  display: grid;
  gap: 10px;
  margin-top: 16px;
}

.document-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  padding: 12px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #ffffff;
  color: #4b5563;
  font-size: 13px;
  overflow-wrap: anywhere;
}

.document-item strong {
  color: #111827;
  font-size: 14px;
}

.document-info {
  flex: 1;
}

.document-info p {
  margin: 6px 0 0;
}

.document-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.danger-button {
  margin-top: 0;
  padding: 8px 12px;
  border-radius: 10px;
  background: #fee2e2;
  color: #991b1b;
  font-size: 14px;
}

.danger-button:hover {
  background: #fecaca;
}

.danger-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

textarea {
  width: 100%;
  min-height: 120px;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 16px;
  resize: vertical;
  box-sizing: border-box;
}

textarea:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

button {
  margin-top: 16px;
  padding: 12px 22px;
  border: none;
  border-radius: 12px;
  background: #111827;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background: #374151;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.loading-text {
  margin-top: 14px;
  color: #4b5563;
  font-size: 14px;
}

.answer-box {
  margin-top: 28px;
  padding: 20px;
  border-radius: 12px;
  background: #f3f4f6;
}

.answer-box h2 {
  margin-top: 0;
}

.retrieval-box {
  margin-top: 18px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #ffffff;
}

.retrieval-box h2 {
  margin-top: 0;
  font-size: 20px;
}

.retrieval-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.retrieval-grid div {
  padding: 12px;
  border-radius: 10px;
  background: #f9fafb;
}

.retrieval-grid span {
  display: block;
  margin-bottom: 6px;
  color: #6b7280;
  font-size: 13px;
}

.retrieval-grid strong {
  color: #111827;
  font-size: 15px;
}

.error-box {
  margin-top: 20px;
  padding: 14px;
  border-radius: 12px;
  background: #fee2e2;
  color: #991b1b;
}

.sources-box {
  margin-top: 24px;
}

.sources-box h2 {
  font-size: 20px;
  margin-bottom: 14px;
}

.no-sources {
  margin-top: 16px;
  color: #6b7280;
  font-size: 14px;
}

.source-item {
  padding: 16px;
  margin-bottom: 14px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #ffffff;
}

.source-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 10px;
}

.source-detail {
  margin-top: 10px;
}

.source-detail summary {
  cursor: pointer;
  color: #111827;
  font-weight: 500;
}

.source-text {
  margin-top: 10px;
  color: #374151;
  line-height: 1.7;
  white-space: pre-wrap;
}
</style>
