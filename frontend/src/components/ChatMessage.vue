<script setup lang="ts">
import { isTravelPlan, type ChatMessage } from '../types'
import TravelPlanView from './TravelPlanView.vue'

defineProps<{ message: ChatMessage }>()
</script>

<template>
  <div :class="['message-row', message.role]">
    <div v-if="message.role === 'assistant'" class="assistant-avatar">T</div>
    <div class="message-body">
      <TravelPlanView v-if="isTravelPlan(message.content)" :plan="message.content" />
      <div v-else class="message-bubble">
        {{ typeof message.content === 'string' ? message.content : message.content.message }}
      </div>
      <time>{{ new Date(message.createdAt).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) }}</time>
    </div>
  </div>
</template>
