<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import draggable from 'vuedraggable'
import { useTripStore } from '../stores/trip'
import type { ItineraryItem } from '../types'
import ItineraryCard from '../components/ItineraryCard.vue'
import ItineraryEditor from '../components/ItineraryEditor.vue'

const store = useTripStore()
const editorOpen = ref(false)
const editing = ref<ItineraryItem | null>(null)
const totalBudget = computed(() => store.itinerary.reduce((total, item) => total + Number(item.budget || 0), 0))
const budgetItems = computed(() => {
  const budget = store.travelPlan?.budget_breakdown
  if (!budget) return []
  return [
    ['交通', budget.transportation],
    ['住宿', budget.accommodation],
    ['餐饮', budget.food],
    ['游玩', budget.entertainment],
    ['其他', budget.misc],
  ] as const
})

function selectPlan(event: Event) {
  editorOpen.value = false
  store.selectConversation((event.target as HTMLSelectElement).value)
}

onMounted(async () => {
  await store.initialize()
  if (!store.travelPlan && store.travelConversations.length) {
    await store.selectConversation(store.travelConversations[0].id)
  }
})

function openEditor(item: ItineraryItem | null = null) {
  editing.value = item ? { ...item } : null
  editorOpen.value = true
}

async function save(item: ItineraryItem | Omit<ItineraryItem, 'id'>) {
  const saved = 'id' in item
    ? await store.updateItinerary(item)
    : await store.addItinerary(item)
  if (saved) editorOpen.value = false
}
</script>

<template>
  <div class="itinerary-page page-container">
    <header class="page-heading">
      <div><span class="welcome-kicker">YOUR TRIP, YOUR RHYTHM</span><h1>行程管理</h1><p>拖动卡片调整顺序，按自己的节奏继续完善旅程。</p></div>
      <button class="add-button" type="button" @click="openEditor()">＋ 添加行程</button>
    </header>

    <div class="trip-selector">
      <label for="current-trip">当前行程</label>
      <div class="select-wrap">
        <select
          id="current-trip"
          :value="store.activeConversationId"
          :disabled="!store.travelConversations.length"
          @change="selectPlan"
        >
          <option v-if="!store.travelConversations.length" value="">尚未生成旅行方案</option>
          <option v-for="conversation in store.travelConversations" :key="conversation.id" :value="conversation.id">
            {{ conversation.title }}
          </option>
        </select>
      </div>
    </div>

    <p v-if="store.error" class="error-message itinerary-error">{{ store.error }}</p>

    <div class="summary-strip">
      <div><small>目的地</small><strong>{{ store.travelPlan?.destination || '尚未生成' }}</strong></div>
      <div><small>行程天数</small><strong>{{ store.travelPlan ? `${store.travelPlan.days} 天` : '—' }}</strong></div>
      <div><small>当前预算</small><strong>¥{{ totalBudget.toLocaleString('zh-CN') }}</strong></div>
      <span>已保存旅行方案</span>
    </div>

    <div v-if="!store.itinerary.length" class="itinerary-empty">
      <span>⌁</span><h2>这里还没有行程</h2><p>先让 AI 生成旅行计划，或手动添加第一张行程卡片。</p>
      <div><RouterLink to="/" class="secondary-link">去问 AI</RouterLink><button type="button" @click="openEditor()">手动添加</button></div>
    </div>

    <draggable v-else v-model="store.itinerary" class="itinerary-list" handle=".drag-handle" :animation="220" ghost-class="drag-ghost" item-key="id" @start="store.beginItineraryReorder" @end="store.saveItineraryOrder">
      <template #item="{ element, index }">
        <ItineraryCard :item="element" :index="index" @edit="openEditor" @remove="store.removeItinerary" />
      </template>
    </draggable>

    <div v-if="store.travelPlan" class="plan-extras">
      <section class="plan-extra-card">
        <span class="eyebrow">LOCAL FLAVORS</span>
        <h2>美食推荐</h2>
        <div class="food-tags"><span v-for="food in store.travelPlan.food" :key="food">{{ food }}</span></div>
      </section>
      <section class="plan-extra-card">
        <span class="eyebrow">BUDGET</span>
        <div class="extra-heading"><h2>预算分配</h2><strong>¥{{ store.travelPlan.budget_breakdown.total_estimated.toLocaleString('zh-CN') }}</strong></div>
        <div class="budget-grid">
          <div v-for="([label, value]) in budgetItems" :key="label"><span>{{ label }}</span><strong>¥{{ value.toLocaleString('zh-CN') }}</strong></div>
        </div>
      </section>
    </div>

    <ItineraryEditor v-if="editorOpen" :item="editing" :next-day="store.itinerary.length + 1" @save="save" @close="editorOpen = false" />
  </div>
</template>
