<template>
  <div class="container-fluid">
    <div class="row">
      <button
        class="btn toggle-btn px-2 py-1"
        type="button"
        @click="toggleSidebar"
      >
        ☰
      </button>

      <nav
        class="col-md-3 col-lg-2 sidebar"
        :class="{ 'sidebar-open': isSidebarOpen }"
        >
        <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
          <div class="h5 mb-0 mx-auto pe-4 fw-bold">
            <div>{{ roleDisplayName }}</div>
          </div>
        </div>
        <hr>

        <ul class="nav flex-column text-center">
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Profile' }" @click="toggleSidebar">Profile</router-link>
          </li>

          <template v-if="isAdmin">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Dashboard' }" @click="toggleSidebar">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Orders' }" @click="toggleSidebar">Orders</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Cars' }" @click="toggleSidebar">Cars</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Staff' }" @click="toggleSidebar">Staff</router-link>
            </li>
          </template>

          <template v-else-if="isStaff">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Dashboard' }" @click="toggleSidebar">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Orders' }" @click="toggleSidebar">My orders</router-link>
            </li>
          </template>

          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Orders' }" @click="toggleSidebar">My orders</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Cars' }" @click="toggleSidebar">Cars</router-link>
            </li>
          </template>

          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Logout' }" @click="toggleSidebar">Logout</router-link>
          </li>
        </ul>
      </nav>

      <div class="col-md-9 col-lg-10 content-area">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const isSidebarOpen = ref(false);

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const isAdmin = computed(() => {
  return ['manager', 'admin'].includes(authStore.user?.role);
});

const isStaff = computed(() => {
  return ['mechanic'].includes(authStore.user?.role);
});

const roleDisplayName = computed(() => {
  return isStaff.value || isAdmin.value ? 'Staff' : 'Client';
});
</script>

<style scoped>
.container-fluid, .row {
  height: 100%;
}

.sidebar {
  height: 100%;
  border-right: 1px solid lightgray;
  position: sticky;
  top: 0;
  z-index: 1035;
  padding: 0;
  background-color: white;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 280px;
    max-width: 280px;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 1035;
  }
  
  .sidebar-open {
    transform: translateX(0);
  }
}

.nav-link {
  color: black;
  font-size: 17px;
  font-weight: 500;
  transition: background-color 0.1s linear;
}

.nav-link.active {
  background-color: #ddeafc;
  border-radius: 10px;
  color: #3687ff;
}

.content-area {
  padding: 30px 40px;
  flex: 1;
  overflow-y: auto;
}

.toggle-btn {
  position: fixed;
  top: 3px;
  left: 10px;
  z-index: 1050;
  width: auto;
  padding: 8px 12px;
  font-size: 24px;
  background: #0d6efd;
  color: white;
  border: none;
  border-radius: 5px;
  display: none;
}

@media (max-width: 768px) {
  .toggle-btn {
    display: block;
  }
}
</style>