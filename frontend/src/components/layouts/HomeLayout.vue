<template>
  <HomePage />
</template>

<script setup>
import HomePage from '@/views/HomePage.vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { computed } from 'vue';

const router = useRouter();

const isAdmin = computed(() => {
  return ['manager', 'admin'].includes(authStore.user?.role);
});

const isStaff = computed(() => {
  return ['mechanic'].includes(authStore.user?.role);
});

const authStore = useAuthStore();
if (isStaff.value || isAdmin.value) {
  router.push({ name: 'Dashboard' });
} else {
  router.push({ name: 'Orders' })
}
</script>