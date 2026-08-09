<script setup lang="ts">
import { computed } from 'vue'
import { useTripStore } from '../stores/trip'

const store = useTripStore()
const recentMessages = computed(() => store.messages.filter((m) => m.role === 'user').slice(-5).reverse())
</script>

<template>
  <aside class="sidebar">
    <button class="new-chat" type="button" @click="store.newSession">＋ 新建旅行对话</button>

    <section class="side-section">
      <div class="section-label"><span>最近对话</span><small>本地记录</small></div>
      <div v-if="recentMessages.length" class="history-list">
        <button v-for="message in recentMessages" :key="message.id" type="button" class="history-item">
          <span>✦</span><span>{{ String(message.content) }}</span>
        </button>
      </div>
      <div v-else class="side-empty">对话后将在这里显示历史记录</div>
    </section>

    <section class="session-card">
      <div class="section-label"><span>当前 Session</span><i class="status-dot" /></div>
      <strong>{{ store.sessionShortId }}</strong>
      <small>完整 ID 已安全保存在本机</small>
    </section>

    <section class="profile-card">
      <div class="avatar">旅</div>
      <div><strong>旅行探索者</strong><small>偏好：人文 · 美食 · 慢旅行</small></div>
      <span class="mock-tag">模拟</span>
    </section>
  </aside>
</template>
