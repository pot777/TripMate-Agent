<script setup lang="ts">
import type { TravelPlan } from '../types'

defineProps<{ plan: TravelPlan }>()
const money = (value: number) => `¥${Number(value || 0).toLocaleString('zh-CN')}`
</script>

<template>
  <article class="plan-card">
    <div class="plan-heading">
      <div><span class="eyebrow">YOUR JOURNEY</span><h2>{{ plan.destination }}旅行计划</h2></div>
      <div class="plan-meta"><span>{{ plan.days }} 天</span><span>预算 {{ money(plan.budget) }}</span></div>
    </div>

    <div class="day-list">
      <section v-for="item in plan.schedule" :key="item.day" class="day-item">
        <div class="day-number"><small>DAY</small><strong>{{ String(item.day).padStart(2, '0') }}</strong></div>
        <div class="day-content">
          <h3>{{ item.title }}</h3>
          <ul><li v-for="activity in item.activities" :key="activity">{{ activity }}</li></ul>
          <div class="day-notes"><span>交通：{{ item.transportation }}</span><span>住宿：{{ item.accommodation_suggestion }}</span></div>
        </div>
      </section>
    </div>

    <div class="plan-bottom">
      <section><span class="eyebrow">当地风味</span><div class="food-tags"><span v-for="food in plan.food" :key="food">{{ food }}</span></div></section>
      <section class="budget-summary"><span class="eyebrow">预算概览</span><strong>{{ money(plan.budget_breakdown.total_estimated) }}</strong><small>交通 {{ money(plan.budget_breakdown.transportation) }} · 住宿 {{ money(plan.budget_breakdown.accommodation) }} · 餐饮 {{ money(plan.budget_breakdown.food) }}</small></section>
    </div>
  </article>
</template>
