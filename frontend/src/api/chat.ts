import type { AgentAnswer, ChatResponse, Conversation, ConversationDetail, PlanUpdateResponse, TraceEvent, TravelPlan } from '../types'

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { Accept: 'application/json' },
    ...init,
  })

  if (!response.ok) {
    throw new Error(`请求失败（${response.status}）`)
  }

  return response.json() as Promise<T>
}

export async function sendChat(message: string, conversationId: string): Promise<ChatResponse> {
  const query = new URLSearchParams({ message, session_id: conversationId })
  return requestJson<ChatResponse>(`/api/chat?${query.toString()}`)
}

export async function streamChat(
  message: string,
  conversationId: string,
  onTrace: (event: TraceEvent) => void,
): Promise<AgentAnswer> {
  const query = new URLSearchParams({ message, session_id: conversationId })
  const response = await fetch(`/api/chat/stream?${query.toString()}`, {
    headers: { Accept: 'text/event-stream' },
  })

  if (!response.ok || !response.body) {
    throw new Error(`请求失败（${response.status}）`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  let answer: AgentAnswer | undefined

  function processEvent(block: string) {
    let eventName = 'message'
    const dataLines: string[] = []

    for (const line of block.split('\n')) {
      if (line.startsWith('event:')) eventName = line.slice(6).trim()
      if (line.startsWith('data:')) dataLines.push(line.slice(5).trimStart())
    }

    if (!dataLines.length) return
    const payload = JSON.parse(dataLines.join('\n')) as Record<string, unknown>
    const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false })

    if (eventName === 'trace') {
      console.info(`[${timestamp}] received ${String(payload.name || 'trace')}`)
      onTrace(payload as unknown as TraceEvent)
    } else if (eventName === 'result') {
      console.info(`[${timestamp}] received result`)
      answer = payload.answer as AgentAnswer
    } else if (eventName === 'error') {
      console.info(`[${timestamp}] received error`)
      throw new Error(typeof payload.message === 'string' ? payload.message : '旅行规划失败，请稍后重试')
    }
  }

  while (true) {
    const { value, done } = await reader.read()
    buffer += decoder.decode(value, { stream: !done }).replace(/\r\n/g, '\n')

    let boundary = buffer.indexOf('\n\n')
    while (boundary >= 0) {
      processEvent(buffer.slice(0, boundary))
      buffer = buffer.slice(boundary + 2)
      boundary = buffer.indexOf('\n\n')
    }

    if (done) break
  }

  if (buffer.trim()) processEvent(buffer)
  if (answer === undefined) throw new Error('旅行规划未返回结果，请稍后重试')
  return answer
}

export function getConversations(): Promise<Conversation[]> {
  return requestJson<Conversation[]>('/api/conversations')
}

export function getConversation(conversationId: string): Promise<ConversationDetail> {
  return requestJson<ConversationDetail>(`/api/conversations/${encodeURIComponent(conversationId)}`)
}

export function updateConversationPlan(conversationId: string, plan: TravelPlan): Promise<PlanUpdateResponse> {
  return requestJson<PlanUpdateResponse>(`/api/conversations/${encodeURIComponent(conversationId)}/plan`, {
    method: 'PUT',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(plan),
  })
}
