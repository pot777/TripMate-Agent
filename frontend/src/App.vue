<script setup lang="ts">
import AppTabBar from './components/AppTabBar.vue'
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <RouterLink class="brand" to="/">
        <span class="brand-mark">T</span>
        <span><strong>TripMate</strong><small>你的智能旅行搭子</small></span>
      </RouterLink>
      <div class="online"><i /> AI 服务已连接</div>
    </header>
    <main><RouterView /></main>
    <AppTabBar />
  </div>
</template>
