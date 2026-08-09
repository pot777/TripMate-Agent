import { computed, ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { sendChat } from '../api/chat'
import { isTravelPlan, type AgentAnswer, type ChatMessage, type ItineraryItem, type TravelPlan } from '../types'

const STORAGE_KEY = 'tripmate-demo-state'
const makeId = () => crypto.randomUUID()

interface SavedState {
  sessionId: string
  messages: ChatMessage[]
  plan: TravelPlan | null
  itinerary: ItineraryItem[]
}

function loadState(): SavedState | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export const useTripStore = defineStore('trip', () => {
  const saved = loadState()
  const sessionId = ref(saved?.sessionId || makeId())
  const messages = ref<ChatMessage[]>(saved?.messages || [])
  const travelPlan = ref<TravelPlan | null>(saved?.plan || null)
  const itinerary = ref<ItineraryItem[]>(saved?.itinerary || [])
  const loading = ref(false)
  const error = ref('')

  const sessionShortId = computed(() => sessionId.value.slice(0, 8).toUpperCase())

  watch([sessionId, messages, travelPlan, itinerary], () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      sessionId: sessionId.value,
      messages: messages.value,
      plan: travelPlan.value,
      itinerary: itinerary.value,
    }))
  }, { deep: true })

  function planToItinerary(plan: TravelPlan): ItineraryItem[] {
    const dailyBudget = Math.round((plan.budget_breakdown.total_estimated || plan.budget) / Math.max(plan.days, 1))
    return plan.schedule.map((item) => ({
      id: makeId(),
      day: item.day,
      dateTime: `第 ${item.day} 天`,
      location: plan.destination,
      content: [item.title, ...item.activities].filter(Boolean).join(' · '),
      transportation: item.transportation,
      budget: dailyBudget,
    }))
  }

  async function submitMessage(text: string) {
    const message = text.trim()
    if (!message || loading.value) return
    error.value = ''
    messages.value.push({ id: makeId(), role: 'user', content: message, createdAt: new Date().toISOString() })
    loading.value = true
    try {
      const response = await sendChat(message, sessionId.value)
      messages.value.push({ id: makeId(), role: 'assistant', content: response.answer, createdAt: new Date().toISOString() })
      if (isTravelPlan(response.answer)) {
        travelPlan.value = response.answer
        itinerary.value = planToItinerary(response.answer)
      }
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : '暂时无法连接旅行助手'
    } finally {
      loading.value = false
    }
  }

  function newSession() {
    sessionId.value = makeId()
    messages.value = []
    travelPlan.value = null
    itinerary.value = []
    error.value = ''
  }

  function addItinerary(item: Omit<ItineraryItem, 'id'>) {
    itinerary.value.push({ ...item, id: makeId() })
  }

  function updateItinerary(item: ItineraryItem) {
    const index = itinerary.value.findIndex((entry) => entry.id === item.id)
    if (index >= 0) itinerary.value[index] = { ...item }
  }

  function removeItinerary(id: string) {
    itinerary.value = itinerary.value.filter((item) => item.id !== id)
  }

  function answerText(answer: AgentAnswer) {
    if (typeof answer === 'string') return answer
    if ('message' in answer) return answer.message
    return `${answer.destination} ${answer.days} 天旅行计划`
  }

  return {
    sessionId, sessionShortId, messages, travelPlan, itinerary, loading, error,
    submitMessage, newSession, addItinerary, updateItinerary, removeItinerary, answerText,
  }
})
