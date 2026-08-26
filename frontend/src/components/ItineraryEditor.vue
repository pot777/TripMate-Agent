<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { ItineraryItem } from '../types'

const props = defineProps<{ item: ItineraryItem | null; nextDay: number }>()
const emit = defineEmits<{ save: [item: ItineraryItem | Omit<ItineraryItem, 'id'>]; close: [] }>()

const form = reactive({ day: 1, dateTime: '', location: '', content: '', transportation: '', accommodationSuggestion: '', budget: 0 })

watch(() => props.item, (item) => {
  Object.assign(form, item || { day: props.nextDay, dateTime: `第 ${props.nextDay} 天`, location: '', content: '', transportation: '', accommodationSuggestion: '', budget: 0 })
}, { immediate: true })

function save() {
  if (!form.location.trim() || !form.content.trim()) return
  emit('save', props.item ? { ...props.item, ...form } : { ...form })
}
</script>

<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <section class="editor-modal" role="dialog" aria-modal="true" aria-labelledby="editor-title">
      <div class="modal-heading"><div><span class="eyebrow">ITINERARY ITEM</span><h2 id="editor-title">{{ item ? '修改行程' : '添加新行程' }}</h2></div><button type="button" @click="$emit('close')">×</button></div>
      <form @submit.prevent="save">
        <label><span>日期 / 时间</span><input v-model="form.dateTime" required placeholder="例如：第 1 天 · 上午 9:00" /></label>
        <label><span>地点</span><input v-model="form.location" required placeholder="例如：成都 · 宽窄巷子" /></label>
        <label class="full"><span>行程内容</span><textarea v-model="form.content" required rows="4" placeholder="描述游览、用餐或休息安排" /></label>
        <label><span>交通方式</span><input v-model="form.transportation" placeholder="例如：地铁 2 号线" /></label>
        <label><span>预算（元）</span><input v-model.number="form.budget" type="number" min="0" step="1" /></label>
        <div class="modal-actions full"><button type="button" class="secondary" @click="$emit('close')">取消</button><button type="submit" class="primary">保存行程</button></div>
      </form>
    </section>
  </div>
</template>
