<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { useTripStore } from '../stores/trip'
import ChatSidebar from '../components/ChatSidebar.vue'
import ChatMessage from '../components/ChatMessage.vue'

const store = useTripStore()
const input = ref('')
const chatEnd = ref<HTMLElement | null>(null)
const suggestions = ['成都 3 天游，预算 3000 元', '周末去上海看展和吃美食', '北京亲子游，行程轻松一点']

async function submit(text = input.value) {
  if (!text.trim()) return
  input.value = ''
  await store.submitMessage(text)
  await nextTick()
  chatEnd.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="home-layout">
    <ChatSidebar />
    <section class="chat-workspace">
      <div v-if="!store.messages.length" class="welcome">
        <span class="welcome-kicker">PLAN LESS · EXPERIENCE MORE</span>
        <h1>下一站，想去哪里？</h1>
        <p>告诉我目的地、时间和预算，我会结合天气与景点信息，为你整理一份专属旅行计划。</p>
        <div class="suggestions">
          <button v-for="suggestion in suggestions" :key="suggestion" type="button" @click="submit(suggestion)">↗ {{ suggestion }}</button>
        </div>
      </div>

      <div v-else class="conversation">
        <ChatMessage v-for="message in store.messages" :key="message.id" :message="message" />
        <div v-if="store.loading" class="message-row assistant"><div class="assistant-avatar">T</div><div class="thinking"><i/><i/><i/><span>正在规划旅程…</span></div></div>
        <div ref="chatEnd" />
      </div>

      <div class="composer-wrap">
        <p v-if="store.error" class="error-message">{{ store.error }}，请确认 FastAPI 已启动后重试。</p>
        <form class="composer" @submit.prevent="submit()">
          <textarea v-model="input" rows="1" placeholder="描述你的旅行需求，例如：10 月去成都玩 3 天，预算 3000 元…" :disabled="store.loading" @keydown.enter.exact.prevent="submit()" />
          <button type="submit" :disabled="!input.trim() || store.loading" aria-label="发送旅行需求">↑</button>
        </form>
        <small>TripMate 可能会生成不准确的信息，请结合实际情况确认。</small>
      </div>
    </section>
  </div>
</template>
