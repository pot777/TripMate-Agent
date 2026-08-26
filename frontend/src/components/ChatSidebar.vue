<script setup lang="ts">
import { useTripStore } from '../stores/trip'

const store = useTripStore()

function formatDate(value: string) {
  const date = new Date(value)
  const today = new Date()
  const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate()).getTime()
  const targetDay = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime()
  const daysAgo = Math.round((startOfToday - targetDay) / 86400000)
  if (daysAgo === 0) return '今天'
  if (daysAgo === 1) return '昨天'
  return `${date.getMonth() + 1}月${date.getDate()}日`
}
</script>

<template>
  <aside class="sidebar">
    <button class="new-chat" type="button" @click="store.newConversation">＋ 新建旅行对话</button>

    <section class="side-section">
      <div class="section-label"><span>最近旅行</span></div>
      <div v-if="store.conversations.length" class="history-list">
        <button
          v-for="conversation in store.conversations"
          :key="conversation.id"
          type="button"
          :class="['history-item', { active: conversation.id === store.activeConversationId }]"
          @click="store.selectConversation(conversation.id)"
        >
          <span class="history-title">{{ conversation.title }}</span>
          <span class="history-preview">{{ conversation.preview }}</span>
          <time>{{ formatDate(conversation.updated_at) }}</time>
        </button>
      </div>
      <div v-else class="side-empty">开始规划后，旅行会显示在这里</div>
    </section>

    <section class="profile-card">
      <div class="avatar">旅</div>
      <div><strong>旅行探索者</strong><small>偏好：人文 · 美食 · 慢旅行</small></div>
      <span class="mock-tag">模拟</span>
    </section>
  </aside>
</template>
