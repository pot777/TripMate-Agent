import type { AgentAnswer, ChatResponse, Conversation, ConversationDetail, PlanUpdateResponse, TraceEvent, TravelPlan } from '../types'

const SSE_IDLE_TIMEOUT_MS = 90_000

class SseBusinessError extends Error {}

interface ErrorPayload {
  detail?: string | { message?: string }
  message?: string
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(path, {
      headers: { Accept: 'application/json' },
      ...init,
    })
  } catch {
    throw new Error('暂时无法连接旅行助手')
  }

  if (!response.ok) {
    if (response.status === 404) throw new Error('这次旅行记录已失效，请重新选择')

    let payload: ErrorPayload | null = null
    try {
      payload = await response.json() as ErrorPayload
    } catch {
      // Fall back to a safe generic message for non-JSON error responses.
    }
    const safeMessage = typeof payload?.detail === 'string'
      ? payload.detail
      : payload?.detail?.message || payload?.message
    if (safeMessage) throw new Error(safeMessage)
    throw new Error('旅行助手暂时无法处理请求，请稍后重试')
  }

  try {
    return await response.json() as T
  } catch {
    throw new Error('旅行助手返回异常，请稍后重试')
  }
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
  const controller = new AbortController()
  let reader: ReadableStreamDefaultReader<Uint8Array> | null = null
  let timeoutId: ReturnType<typeof setTimeout> | undefined
  let timedOut = false

  const resetTimeout = () => {
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      timedOut = true
      controller.abort()
    }, SSE_IDLE_TIMEOUT_MS)
  }

  resetTimeout()

  try {
    const response = await fetch(`/api/chat/stream?${query.toString()}`, {
      headers: { Accept: 'text/event-stream' },
      signal: controller.signal,
    })

    if (!response.ok || !response.body) {
      if (response.status === 404) throw new SseBusinessError('这次旅行记录已失效，请重新选择')
      throw new SseBusinessError('旅行助手暂时无法处理请求，请稍后重试')
    }

    reader = response.body.getReader()
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
      resetTimeout()
      const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false })

      if (eventName === 'trace') {
        console.info(`[${timestamp}] received ${String(payload.name || 'trace')}`)
        onTrace(payload as unknown as TraceEvent)
      } else if (eventName === 'result') {
        console.info(`[${timestamp}] received result`)
        answer = payload.answer as AgentAnswer
      } else if (eventName === 'error') {
        console.info(`[${timestamp}] received error`)
        throw new SseBusinessError(typeof payload.message === 'string' ? payload.message : '旅行规划失败，请稍后重试')
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
    if (answer === undefined) throw new SseBusinessError('旅行规划未返回结果，请稍后重试')
    return answer
  } catch (cause) {
    if (timedOut) throw new Error('旅行规划时间较长，请稍后重试')
    if (cause instanceof SseBusinessError) throw cause
    if (cause instanceof SyntaxError) throw new Error('旅行助手返回异常，请稍后重试')
    throw new Error('暂时无法连接旅行助手')
  } finally {
    if (timeoutId) clearTimeout(timeoutId)
    if (reader) {
      try {
        await reader.cancel()
      } catch {
        // The stream may already be closed or aborted.
      }
    }
  }
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
