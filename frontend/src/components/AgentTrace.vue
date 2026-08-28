<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { TraceEvent } from '../types'

const props = defineProps<{
  events: TraceEvent[]
  loading?: boolean
  mode?: 'plan' | 'modify'
}>()

const expanded = ref(true)

watch(() => props.loading, (loading) => {
  if (loading) expanded.value = true
})

const title = computed(() => {
  if (props.loading) return props.mode === 'modify' ? '正在调整旅行方案…' : '正在规划你的旅行…'
  return props.events.some((event) => event.name === 'modify_plan')
    ? '旅行方案已更新'
    : '旅行规划已完成'
})
</script>

<template>
  <div class="message-row assistant trace-row">
    <div class="assistant-avatar">T</div>
    <section class="agent-trace">
      <button type="button" class="trace-heading" :aria-expanded="expanded" @click="expanded = !expanded">
        <span><i :class="{ loading }" />{{ title }}</span>
        <b>{{ expanded ? '收起' : '展开' }}</b>
      </button>
      <div v-if="expanded" class="trace-events">
        <p v-for="event in events" :key="`${event.type}-${event.name}`" :class="{ unavailable: event.status === 'unavailable' }">
          <span :class="event.status === 'unavailable' ? 'trace-unavailable' : 'trace-check'">{{ event.status === 'unavailable' ? '—' : '✓' }}</span>{{ event.message }}
        </p>
        <p v-if="loading"><span class="trace-pending">•</span>{{ events.length ? '正在继续处理…' : '正在分析旅行需求' }}</p>
      </div>
    </section>
  </div>
</template>
