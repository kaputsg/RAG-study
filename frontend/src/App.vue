<script setup>
import { ref } from "vue"

// 用户输入的问题
const question = ref("")

// 后端返回的回答
const answer = ref("")

// 后端返回的引用来源
const sources = ref([])

// 加载状态
const loading = ref(false)

// 错误信息
const errorMessage = ref("")

async function handleSubmit() {
  if (!question.value.trim()) {
    answer.value = "请先输入问题。"
    return
  }

  loading.value = true
  answer.value = ""
  sources.value = []
  errorMessage.value = ""

  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
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
    sources.value = data.sources
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}
</script>


<template>
  <main class="page">
    <section class="card">
      <h1>本地知识库 RAG 问答系统</h1>
      <p class="subtitle">输入问题，后续会调用 FastAPI 后端获取回答。</p>

      <!-- TODO 3：写 textarea，使用 v-model 绑定 question -->

      <textarea
        v-model="question"
        placeholder="例如：开发 Python 后端 API 接口服务推荐用什么框架？"
      ></textarea>

      <!-- TODO 4：写 button，点击时调用 handleSubmit -->

      <button @click="handleSubmit" :disabled="loading">
        {{ loading ? "正在思考..." : "提交问题" }}
      </button>

      <div class="error-box" v-if="errorMessage">
        {{ errorMessage }}
      </div>

      <div class="answer-box" v-if="answer">
        <h2>回答</h2>
        <p>{{ answer }}</p>
      </div>

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

          <p class="source-text">{{ source.text }}</p>
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

.answer-box {
  margin-top: 28px;
  padding: 20px;
  border-radius: 12px;
  background: #f3f4f6;
}

.answer-box h2 {
  margin-top: 0;
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

.source-text {
  margin: 0;
  color: #374151;
  line-height: 1.7;
  white-space: pre-wrap;
}
</style>