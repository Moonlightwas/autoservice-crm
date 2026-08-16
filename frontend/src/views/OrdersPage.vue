<template>
  <div class="page">
    <div class="d-flex justify-content-between ">
      <h3>Orders</h3>
      <div v-if="!isMechanic" class="order-buttons">
        <RouterLink :to="{ name: 'OrderCreate' }">
          <button class="btn btn-primary btn-sm">Create order</button>
        </RouterLink>
      </div>
    </div>

    <div class="filter-menu">
      <nav class="navbar navbar-expand bg-light">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li 
                v-for="filter in filters"
                :key="filter.value"
                class="nav-item"
              >
                <a
                  class="nav-link"
                  @click="changeFilter(filter.value)"
                  :class="{ active: activeFilter == filter.value }"
                >
                  {{ filter.label }}
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>

    <div class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Car</th>
            <th>Description</th>
            <th>Status</th>
            <th>Created at</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="order in orders"
            :key="order.id"
            @click="goToOrder(order.id)"
            style="cursor: pointer;"
          >
            <td>{{ order.id }}</td>
            <td>{{ order.car?.brand }} {{ order.car?.model }}</td>
            <td class="description-cell">{{ order.description }}</td>
            <td>
              <span class="baged" :class="getStatusClass(order.status)">
                {{ getStatusLabel(order.status) }}
              </span>
            </td>
            <td>{{ formatDate(order.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationLayout 
      :current-page="currentPage"
      :total-pages="totalPages"
      @page-change="(page) => { currentPage = page; fetchOrders() }"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getOrders } from '@/services/api';
import { useRouter, useRoute } from 'vue-router';
import PaginationLayout from '@/components/layouts/PaginationLayout.vue'
import { useAuthStore } from '@/stores/auth';

const user = useAuthStore();

const router = useRouter();
const route = useRoute();

const orders = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);

const isMechanic = computed(() => {
  return user.role == 'mechanic';
});

const activeFilter = ref('all');
const filters = [
  { label: 'All', value: 'all' },
  { label: 'Pending', value: 'pending' },
  { label: 'Confirmed', value: 'confirmed' },
  { label: 'In Work', value: 'in_work' },
  { label: 'Ready', value: 'ready' },
  { label: 'Payment', value: 'payment' },
  { label: 'Completed', value: 'complited' },
  { label: 'Canceled', value: 'canceled' }
];

const fetchOrders = async () => {
  try {
    const response = await getOrders({ page: currentPage.value, status: activeFilter.value });
    orders.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / 10);

    await router.replace({
      query: {
        page: currentPage.value,
        status: activeFilter.value
      }
    });
  } catch (error) {
    console.error('Error:', error);
  }
};

onMounted(() => {
  const query = route.query;
  const status = query.status;

  if (query.page) currentPage.value = parseInt(query.page);
  if (status) activeFilter.value = status;

  fetchOrders();
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};

const goToOrder = (id) => {
  router.push({ name: 'OrderDetail', params: { id } });
};

const changeFilter = async (filter) => {
  currentPage.value = 1;
  activeFilter.value = filter;

  await router.replace({
    query: {status: activeFilter.value}
  });
  
  fetchOrders();
};

const getStatusLabel = (status) => {
  const labels = {
    pending: 'Pending',
    confirmed: 'Confirmed',
    in_work: 'In Work',
    ready: 'Ready',
    payment: 'Payment',
    complited: 'Completed',
    canceled: 'Canceled'
  }
  return labels[status] || '';
}

const getStatusClass = (status) => {
  const classes = {
    pending: 'text-secondary',
    confirmed: 'text-primary',
    in_work: 'text-warning',
    ready: 'text-warning',
    payment: 'text-success',
    complited: 'text-success',
    canceled: 'text-danger'
  }
  return classes[status] || classes.pending
}
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
}

.filter-menu {
  border-radius: 20px;
  display: inline-block;
}
.filter-menu nav {
  border: 0px solid;
  border-radius: 15px;
  display: inline-block;
}
.filter-menu .container-fluid {
  padding: 0 16px;
}
.navbar-nav {
  gap: 4px;
}
.nav-link {
  cursor: pointer;
  padding: 6px 12px;
  white-space: nowrap;
}
.nav-link.active {
  border-bottom: 3px solid #0d6efd;
}
.nav-link .badge {
  font-size: 10px;
  padding: 2px 6px;
}

.table-wrapper {
  flex: 1;
}
.table tbody tr td {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.table tbody tr:hover td {
  cursor: pointer;
  background-color: #f0f7ff;
  transition: background-color 0.3s ease;
}
.description-cell {
  max-width: 200px;
  overflow-y: hidden;
}
.table span.baged {
  font-size: medium; 
  font-weight: bold;
}
</style>