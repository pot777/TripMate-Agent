import type { ChatResponse, Conversation, ConversationDetail, PlanUpdateResponse, TravelPlan } from '../types'

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
