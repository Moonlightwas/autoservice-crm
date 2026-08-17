<template>
  <div class="container">
    <div class="order-header">
      <div>
        <h3 class="mb-0">Order #{{ order.id }}</h3>
        <div class="row">
          <span class="order-meta">Created {{ formatDate(order.created_at) }}</span>
          <span class="order-meta">Updated {{ formatDate(order.updated_at) }}</span>
        </div>
      </div>
    </div>

    <div class="card p-4">
      <div class="row g-4">

        <div class="col-md-6" >
          <h6 class="text-muted text-uppercase small fw-bold mb-3">Car</h6>
          <div class="d-flex align-items-center gap-3">
            <div class="car-image">
              <i class="bi bi-images"></i>
            </div>
            <div>
              <router-link class="car-header" :to="{ name: 'CarDetail', params: { id: order.car?.id } }">
                <h6 class="mb-1 fw-bold">{{ order.car?.brand }} {{ order.car?.model }}</h6>
              </router-link>
              <div class="text-muted small">
                <div>Year: {{ order.car?.year }}</div>
                <div class="font-monospace mt-1">VIN: {{ order.car?.vin || '—' }}</div>
                <div>Plate: {{ order.car?.plate_number || '—' }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 ps-md-4">
          <h6 class="text-muted text-uppercase small fw-bold mb-3">Info</h6>
          <div class="d-flex justify-content-between">
              <span class="text-muted small">Created at</span> 
              <span class="fw-medium">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="d-flex justify-content-between">
              <span class="text-muted small">Total price</span> 
              <span class="fw-bold fs-5">{{ order.total_price }} ₽</span>
          </div>
          <div class="d-flex justify-content-end" v-if="order.status == 'payment' && isClient">
            <button class="btn btn-primary mt-5">Pay</button>
          </div>
        </div>
      </div>
    </div>

    <div class="row p-4 mb-3">
      <div class="description-header">
        <h6 class="text-muted text-uppercase small fw-bold mb-2">Description</h6>
        <button v-if="isAdmin || isClient" class="btn btn-primary btn-sm">Edit</button>
      </div>
      <p class="mb-0">{{ order?.description || '—' }}</p>
    </div>

    <div class="row p-4 mb-3">
      <h6 class="text-muted text-uppercase small fw-bold mb-3">Order status</h6>
      <div v-if="order.status === 'canceled'" class="canceled-status">
        <span class="canceled-icon">✕</span>
        <span class="canceled-text">Order Canceled</span>
      </div>
      <div v-else class="status-path">
        <div 
          v-for="(step, index) in statusSteps"
          :key="step.key"
          class="status-item"
          >
          <div
            class="status-step"
            :class="{
              active: isActive(step.key), 
              done: isPassed(step.key),
              'admin-hover': isAdmin
            }"
            @click="isAdmin && handleForceUpdate(step.key)"
          >
            <span v-if="isPassed(step.key)">✓</span>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div class="status-info">
            <span class="status-label" :class="{ active: isActive(step.key) }">
              {{ step.label }}
            </span>
            <div class="status-time">
              {{ formatDate(getStatusDate(step.key)) || ' ' }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { getOrder } from '@/services/api';
import { useRoute } from 'vue-router';
import { forceStatus } from '@/services/api';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const user = authStore.user;

const isAdmin = computed(() => {
  return user && ['manager', 'admin'].includes(user.role);
});

const isClient = computed(() => {
  return authStore.user?.role == 'client';
});

const route = useRoute();

const order = ref({});

const statusSteps = [
  { key: 'pending', label: 'Pending' },
  { key: 'confirmed', label: 'Confirmed' },
  { key: 'in_work', label: 'In Work' },
  { key: 'ready', label: 'Ready' },
  { key: 'payment', label: 'Payment' },
  { key: 'complited', label: 'Completed' }
];

const dateFields = {
  confirmed: 'confirmed_at',
  in_work: 'started_at',
  ready: 'ready_at',
  payment: 'confirmed_pay_at',
  complited: 'completed_at',
  canceled: 'canceled_at'
};

const getStatusDate = (statusKey) => {
  const field = dateFields[statusKey];
  if (!field) return null;
  return order.value[field] || null;
};


const fetchOrder = async () => {
  const id = route.params.id;
  try {
    const response = await getOrder(id);
    order.value = response.data;
  } catch (error) {
    console.error('Error:', error);
  }
};

onMounted(fetchOrder);


const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const handleForceUpdate = async (new_status) => {
  try{
    if (confirm(`Are you want to change status from "${order.value.status}" to "${new_status}"`)) {
      await forceStatus(order.value.id, {status : new_status});
      await fetchOrder();
    }
  } catch(err) {
    alert(err);
  }
};

const isActive = (status) => order.value?.status === status;
const isPassed = (status) => {
  const current = statusSteps.findIndex(s => s.key === order.value?.status);
  const target = statusSteps.findIndex(s => s.key === status);
  return current >= target;
};
</script>

<style scoped>
.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}
.order-meta {
  padding: 2px 12px 2px 12px;
  font-size: 13px;
  font-weight: 500;
  color: #6c757d;
}

.car-header {
  color: black;
  text-decoration: none;
}

.description-header {
  display: flex;
  justify-content: space-between;
}

.status-path {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
}
.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  min-width: 44px;
}
.status-step {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #edf0f5;
  color: #8b95a9;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s ease;
}
.status-step.done {
  background: #0d6efd;
  color: #fff;
}
.status-step.active {
  background: #0d6efd;
  color: #fff;
  box-shadow: 0 0 0 5px rgba(13,110,253,0.18);
}
.admin-hover:hover {
  cursor: pointer;
  transform: scale(1.1);
}

.status-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.status-label {
  font-size: 13px;
  color: #8b95a9;
  margin-top: 6px;
  white-space: nowrap;
  font-weight: 500;
}
.status-label.active {
  color: #06112a;
}
.status-time {
  font-size: 12px;
  color: #6c757d;
  margin-top: 2px;
  white-space: nowrap;
}

.canceled-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 0;
  gap: 10px;
}
.canceled-icon {
  font-size: 48px;
  color: #dc3545;
  font-weight: 300;
}
.canceled-text {
  font-size: 20px;
  font-weight: 600;
  color: #dc3545;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>