import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { getConversation, getConversations, streamChat, updateConversationPlan } from '../api/chat'
import {
  isTravelPlan,
  type AgentAnswer,
  type ChatMessage,
  type Conversation,
  type ConversationDetail,
  type ItineraryItem,
  type TraceEvent,
  type TravelPlan,
} from '../types'

const makeId = () => crypto.randomUUID()

export const useTripStore = defineStore('trip', () => {
  const conversations = ref<Conversation[]>([])
  const activeConversationId = ref('')
  const messages = ref<ChatMessage[]>([])
  const travelPlan = ref<TravelPlan | null>(null)
  const itinerary = ref<ItineraryItem[]>([])
  const loading = ref(false)
  const currentTrace = ref<TraceEvent[]>([])
  const traceMode = ref<'plan' | 'modify'>('plan')
  const historyLoading = ref(false)
  const initialized = ref(false)
  const savingPlan = ref(false)
  const error = ref('')
  const reorderSnapshot = ref<ItineraryItem[] | null>(null)

  // The list endpoint currently exposes conversation metadata only. Details are
  // always fetched before a selected item is rendered.
  const travelConversations = computed(() => conversations.value)

  function planToItinerary(plan: TravelPlan): ItineraryItem[] {
    const dailyBudget = Math.round((plan.budget_breakdown.total_estimated || plan.budget) / Math.max(plan.days, 1))
    return plan.schedule.map((item) => ({
      id: makeId(),
      day: item.day,
      dateTime: `第 ${item.day} 天`,
      location: item.title || plan.destination,
      content: item.activities.length ? item.activities.join(' · ') : item.title,
      transportation: item.transportation,
      accommodationSuggestion: item.accommodation_suggestion,
      budget: dailyBudget,
    }))
  }

  function itineraryToPlan(items: ItineraryItem[]): TravelPlan {
    if (!travelPlan.value) throw new Error('请先生成旅行方案')

    const totalEstimated = items.reduce((total, item) => total + Number(item.budget || 0), 0)

    return {
      ...travelPlan.value,
      days: Math.max(items.length, 1),
      schedule: items.map((item, index) => ({
        day: index + 1,
        title: item.location.trim() || `${travelPlan.value!.destination}第${index + 1}天`,
        activities: item.content
          .split(/\s*·\s*|\r?\n/)
          .map((activity) => activity.trim())
          .filter(Boolean),
        transportation: item.transportation,
        accommodation_suggestion: item.accommodationSuggestion,
      })),
      budget_breakdown: {
        ...travelPlan.value.budget_breakdown,
        total_estimated: totalEstimated,
      },
    }
  }

  function replaceDisplayedPlan(plan: TravelPlan) {
    for (let index = messages.value.length - 1; index >= 0; index -= 1) {
      const message = messages.value[index]
      if (message.role === 'assistant' && isTravelPlan(message.content)) {
        messages.value[index] = { ...message, content: plan }
        break
      }
    }
  }

  async function persistItinerary(nextItems: ItineraryItem[], previousItems: ItineraryItem[]) {
    if (!activeConversationId.value || !travelPlan.value || savingPlan.value) {
      error.value = travelPlan.value ? '行程正在保存，请稍后再试' : '请先生成旅行方案'
      return false
    }

    const previousPlan = travelPlan.value
    itinerary.value = nextItems
    savingPlan.value = true
    error.value = ''

    try {
      const plan = itineraryToPlan(nextItems)
      const response = await updateConversationPlan(activeConversationId.value, plan)
      travelPlan.value = response.current_plan
      itinerary.value = planToItinerary(response.current_plan)
      replaceDisplayedPlan(response.current_plan)
      await refreshConversations()
      return true
    } catch (cause) {
      travelPlan.value = previousPlan
      itinerary.value = previousItems
      error.value = cause instanceof Error ? `行程保存失败：${cause.message}` : '行程保存失败，请稍后重试'
      return false
    } finally {
      savingPlan.value = false
    }
  }

  function normalizeAssistantContent(content: unknown, plan: TravelPlan | null): AgentAnswer {
    let value = content

    if (typeof value === 'string') {
      const rawContent = value
      try {
        value = JSON.parse(rawContent)
      } catch {
        const legacyMessage = rawContent.match(/['"]message['"]\s*:\s*(['"])(.*?)\1/)?.[2]
        return legacyMessage || rawContent
      }
    }

    if (typeof value !== 'object' || value === null) return String(value ?? '')
    if (isTravelPlan(value as AgentAnswer)) return plan || value as TravelPlan

    const record = value as Record<string, unknown>
    if (typeof record.answer === 'string') return record.answer
    if (record.status === 'need_information' && typeof record.message === 'string') {
      return { status: 'need_information', message: record.message }
    }
    if (record.status === 'error' && typeof record.message === 'string') {
      return { status: 'error', message: record.message }
    }
    if (typeof record.message === 'string') return record.message

    return JSON.stringify(value)
  }

  function messagesFromDetail(detail: ConversationDetail, plan: TravelPlan | null): ChatMessage[] {
    const restored: ChatMessage[] = detail.messages.map((message) => ({
      id: String(message.id),
      role: message.role,
      content: message.role === 'assistant'
        ? normalizeAssistantContent(message.content, plan)
        : typeof message.content === 'string' ? message.content : JSON.stringify(message.content),
      createdAt: message.created_at,
    }))

    if (!plan) return restored

    let planMessageIndex = -1
    for (let index = restored.length - 1; index >= 0; index -= 1) {
      const message = restored[index]
      if (
        message.role === 'assistant'
        && (
          isTravelPlan(message.content)
          || (
            typeof message.content === 'string'
            && message.content.includes('budget_breakdown')
            && message.content.includes('destination')
          )
        )
      ) {
        planMessageIndex = index
        break
      }
    }

    if (planMessageIndex >= 0) {
      restored[planMessageIndex] = {
        ...restored[planMessageIndex],
        content: plan,
      }
    } else {
      restored.push({
        id: `plan-${detail.id}`,
        role: 'assistant',
        content: plan,
        createdAt: detail.updated_at,
      })
    }

    return restored
  }

  function applyConversationDetail(detail: ConversationDetail) {
    const plan = detail.current_plan || detail.travel_state?.current_plan || null
    activeConversationId.value = detail.id
    travelPlan.value = plan
    itinerary.value = plan ? planToItinerary(plan) : []
    messages.value = messagesFromDetail(detail, plan)
  }

  async function refreshConversations() {
    conversations.value = await getConversations()
  }

  async function selectConversation(id: string) {
    if (!id || loading.value) return
    historyLoading.value = true
    currentTrace.value = []
    error.value = ''
    try {
      const detail = await getConversation(id)
      applyConversationDetail(detail)
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : '无法加载历史旅行'
    } finally {
      historyLoading.value = false
    }
  }

  async function initialize() {
    if (initialized.value) return
    initialized.value = true
    historyLoading.value = true
    error.value = ''
    try {
      await refreshConversations()
      if (conversations.value.length) {
        const detail = await getConversation(conversations.value[0].id)
        applyConversationDetail(detail)
      } else {
        newConversation()
      }
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : '无法加载历史旅行'
      if (!activeConversationId.value) newConversation()
    } finally {
      historyLoading.value = false
    }
  }

  async function submitMessage(text: string) {
    const message = text.trim()
    if (!message || loading.value) return
    const conversationId = activeConversationId.value || makeId()
    traceMode.value = travelPlan.value ? 'modify' : 'plan'
    currentTrace.value = []
    activeConversationId.value = conversationId
    error.value = ''
    messages.value.push({
      id: `pending-${makeId()}`,
      role: 'user',
      content: message,
      createdAt: new Date().toISOString(),
    })
    loading.value = true
    try {
      await streamChat(message, conversationId, (event) => {
        if (!currentTrace.value.some((item) => item.name === event.name)) {
          currentTrace.value.push(event)
        }
      })
      await refreshConversations()
      const detail = await getConversation(conversationId)
      applyConversationDetail(detail)
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : '暂时无法连接旅行助手'
      try {
        await refreshConversations()
        if (conversations.value.some((item) => item.id === conversationId)) {
          const detail = await getConversation(conversationId)
          applyConversationDetail(detail)
        }
      } catch {
        // Keep the optimistic message visible while showing the original error.
      }
    } finally {
      loading.value = false
    }
  }

  function newConversation() {
    activeConversationId.value = makeId()
    messages.value = []
    travelPlan.value = null
    itinerary.value = []
    currentTrace.value = []
    traceMode.value = 'plan'
    error.value = ''
  }

  async function addItinerary(item: Omit<ItineraryItem, 'id'>) {
    const previous = itinerary.value.map((entry) => ({ ...entry }))
    const next = [...previous, { ...item, id: makeId() }]
    return persistItinerary(next, previous)
  }

  async function updateItinerary(item: ItineraryItem) {
    const previous = itinerary.value.map((entry) => ({ ...entry }))
    const next = previous.map((entry) => entry.id === item.id ? { ...item } : entry)
    return persistItinerary(next, previous)
  }

  async function removeItinerary(id: string) {
    const previous = itinerary.value.map((entry) => ({ ...entry }))
    const next = previous.filter((item) => item.id !== id)
    return persistItinerary(next, previous)
  }

  function beginItineraryReorder() {
    reorderSnapshot.value = itinerary.value.map((item) => ({ ...item }))
  }

  async function saveItineraryOrder() {
    const previous = reorderSnapshot.value
    reorderSnapshot.value = null
    if (!previous) return false
    const next = itinerary.value.map((item) => ({ ...item }))
    return persistItinerary(next, previous)
  }

  function answerText(answer: AgentAnswer) {
    if (typeof answer === 'string') return answer
    if ('message' in answer) return answer.message
    return `${answer.destination} ${answer.days} 天旅行计划`
  }

  return {
    activeConversationId, conversations, travelConversations,
    messages, travelPlan, itinerary, loading, historyLoading, savingPlan, error,
    currentTrace, traceMode,
    initialize, refreshConversations, submitMessage, newConversation, selectConversation,
    addItinerary, updateItinerary, removeItinerary,
    beginItineraryReorder, saveItineraryOrder, answerText,
  }
})
