<script setup>
import { ref, nextTick } from 'vue'
import { useBaseURL } from '../stores/counter.js'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const BaseStore = useBaseURL()
const BaseURL = BaseStore.getBaseURL()

const input = ref('')
const messages = ref([])
const chatContainer = ref(null)
const isStreaming = ref(false)

/* ---------------------------
   Markdown Configuration
---------------------------- */

marked.setOptions({
  breaks: true,
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  }
})

const renderMarkdown = (content) => {
  const raw = marked.parse(content)
  return DOMPurify.sanitize(raw)
}

/* ---------------------------
   Scroll
---------------------------- */

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

/* ---------------------------
   Send Message
---------------------------- */

const sendMessage = async () => {
  if (!input.value.trim() || isStreaming.value) return

  const userMessage = input.value.trim()

  messages.value.push({
    role: 'user',
    content: userMessage
  })

  input.value = ''
  isStreaming.value = true

  const assistantMessage = {
    role: 'assistant',
    content: '',
    loading: true
  }

  messages.value.push(assistantMessage)

  await scrollToBottom()

  try {
    const response = await fetch(`${BaseURL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userMessage,
        history: messages.value
          .filter(m => m.content)
          .map(m => ({ role: m.role, content: m.content }))
      })
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const parts = buffer.split("\n\n")
      buffer = parts.pop()

      for (const part of parts) {
        if (part.startsWith("data:")) {
          const text = part.replace("data:", "")
          assistantMessage.content += text
        }
      }

      await scrollToBottom()
    }

  } catch (err) {
    assistantMessage.content = "Error connecting to server."
  }

  assistantMessage.loading = false
  isStreaming.value = false
}
</script>

<template>
  <div class="h-screen flex flex-col bg-gray-900 text-white">
    
    <div ref="chatContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
      <div 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="msg.role === 'user' ? 'text-right' : 'text-left'"
      >
      <div 
        class="inline-block px-4 py-2 rounded-xl max-w-2xl prose prose-invert"
        :class="msg.role === 'user' 
          ? 'bg-blue-600'
          : msg.loading
            ? 'bg-red-600 animate-pulse'
            : 'bg-red-600'"
      >
        <div v-html="renderMarkdown(msg.content)" />
      </div>

        <!-- Typing cursor while streaming -->
        <span v-if="msg.role === 'assistant' && msg.loading">
          |
        </span>
      </div>
    </div>

    <div class="p-4 bg-gray-800 flex gap-2">
      <input 
        v-model="input"
        @keyup.enter="sendMessage"
        :disabled="isStreaming"
        class="flex-1 p-2 rounded bg-gray-700 disabled:opacity-50"
        placeholder="Ask Red..."
      />
      <button 
        @click="sendMessage"
        :disabled="isStreaming"
        class="bg-red-500 px-4 rounded hover:bg-red-400 disabled:opacity-50"
      >
        Send
      </button>
    </div>

  </div>
</template>