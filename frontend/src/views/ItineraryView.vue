<script setup lang="ts">
import { computed, ref } from 'vue'
import draggable from 'vuedraggable'
import { useTripStore } from '../stores/trip'
import type { ItineraryItem } from '../types'
import ItineraryCard from '../components/ItineraryCard.vue'
import ItineraryEditor from '../components/ItineraryEditor.vue'

const store = useTripStore()
const editorOpen = ref(false)
const editing = ref<ItineraryItem | null>(null)
const totalBudget = computed(() => store.itinerary.reduce((total, item) => total + Number(item.budget || 0), 0))

function openEditor(item: ItineraryItem | null = null) {
  editing.value = item ? { ...item } : null
  editorOpen.value = true
}

function save(item: ItineraryItem | Omit<ItineraryItem, 'id'>) {
  if ('id' in item) store.updateItinerary(item)
  else store.addItinerary(item)
  editorOpen.value = false
}
</script>

<template>
  <div class="itinerary-page page-container">
    <header class="page-heading">
      <div><span class="welcome-kicker">YOUR TRIP, YOUR RHYTHM</span><h1>行程管理</h1><p>拖动卡片调整顺序，按自己的节奏继续完善旅程。</p></div>
      <button class="add-button" type="button" @click="openEditor()">＋ 添加行程</button>
    </header>

    <div class="summary-strip">
      <div><small>目的地</small><strong>{{ store.travelPlan?.destination || '尚未生成' }}</strong></div>
      <div><small>行程数量</small><strong>{{ store.itinerary.length }} 项</strong></div>
      <div><small>当前预算</small><strong>¥{{ totalBudget.toLocaleString('zh-CN') }}</strong></div>
      <span>仅保存在本机</span>
    </div>

    <div v-if="!store.itinerary.length" class="itinerary-empty">
      <span>⌁</span><h2>这里还没有行程</h2><p>先让 AI 生成旅行计划，或手动添加第一张行程卡片。</p>
      <div><RouterLink to="/" class="secondary-link">去问 AI</RouterLink><button type="button" @click="openEditor()">手动添加</button></div>
    </div>

    <draggable v-else v-model="store.itinerary" class="itinerary-list" handle=".drag-handle" :animation="220" ghost-class="drag-ghost" item-key="id">
      <template #item="{ element, index }">
        <ItineraryCard :item="element" :index="index" @edit="openEditor" @remove="store.removeItinerary" />
      </template>
    </draggable>

    <ItineraryEditor v-if="editorOpen" :item="editing" :next-day="store.itinerary.length + 1" @save="save" @close="editorOpen = false" />
  </div>
</template>
