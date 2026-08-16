<template>
  <app-header />

  <main class="main-content">
    <SidebarLayout v-if="authStore.isAuthenticated && $route.meta.requiresAuth === true">
      <router-view />
    </SidebarLayout>

    <router-view v-else />
  </main>

  <app-footer />
</template>

<script setup>
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';
import SidebarLayout from './components/layouts/SidebarLayout.vue';
import { useAuthStore } from '@/stores/auth';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { onMounted } from 'vue';

const authStore = useAuthStore();

onMounted(async () =>{
  await authStore.init();
}); 
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1 0 auto;
}
</style>