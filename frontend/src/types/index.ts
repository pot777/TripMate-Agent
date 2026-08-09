export interface ScheduleItem {
  day: number
  title: string
  activities: string[]
  transportation: string
  accommodation_suggestion: string
}

export interface BudgetBreakdown {
  transportation: number
  accommodation: number
  food: number
  entertainment: number
  misc: number
  total_estimated: number
}

export interface TravelPlan {
  destination: string
  days: number
  budget: number
  schedule: ScheduleItem[]
  food: string[]
  budget_breakdown: BudgetBreakdown
}

export interface NeedInformation {
  status: 'need_information'
  message: string
}

export interface AgentError {
  status: 'error'
  message: string
}

export type AgentAnswer = string | NeedInformation | AgentError | TravelPlan

export interface ChatResponse {
  user: string
  answer: AgentAnswer
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: AgentAnswer
  createdAt: string
}

export interface ItineraryItem {
  id: string
  day: number
  dateTime: string
  location: string
  content: string
  transportation: string
  budget: number
}

export function isTravelPlan(value: AgentAnswer): value is TravelPlan {
  return typeof value === 'object' && value !== null && 'schedule' in value && 'budget_breakdown' in value
}
