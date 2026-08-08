<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark text-white">
      <div class="container">
        <a class="navbar-brand" href="/">
          AutoService
        </a>

        <ul class="navbar-nav ms-auto">
          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Register' }">Sign Up</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Login' }">Sign In</router-link>
            </li>
          </template>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'AppHeader'
};
</script>

<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>


<style>
.navbar-brand img{
  height: 30px;
  width: auto;
}
</style>