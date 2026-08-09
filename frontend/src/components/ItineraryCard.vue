<script setup lang="ts">
import type { ItineraryItem } from '../types'

defineProps<{ item: ItineraryItem; index: number }>()
defineEmits<{ edit: [item: ItineraryItem]; remove: [id: string] }>()
</script>

<template>
  <article class="itinerary-card">
    <div class="drag-handle" title="拖动调整顺序">⠿</div>
    <div class="timeline-badge"><small>DAY</small><strong>{{ String(index + 1).padStart(2, '0') }}</strong></div>
    <div class="itinerary-main">
      <div class="itinerary-title"><div><span>{{ item.dateTime }}</span><h3>{{ item.location }}</h3></div><strong>¥{{ item.budget.toLocaleString('zh-CN') }}</strong></div>
      <p>{{ item.content }}</p>
      <div class="transport">→ {{ item.transportation || '交通方式待补充' }}</div>
    </div>
    <div class="card-actions">
      <button type="button" aria-label="编辑行程" @click="$emit('edit', item)">编辑</button>
      <button type="button" class="danger" aria-label="删除行程" @click="$emit('remove', item.id)">删除</button>
    </div>
  </article>
</template>
