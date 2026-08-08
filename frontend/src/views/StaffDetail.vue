<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="mb-0">Profile</h3>
    </div>

    <div class="card p-4">
      <div class="d-flex align-items-start gap-4">
        <div class="profile-image">
          {{ staff.email?.[0].toUpperCase() || '?' }}
        </div>

        <div class="flex-grow-1">
          <div class="row g-2">
            <div class="col-md-6">
              <label class="form-label">Email</label>
              <input v-model="staff.email" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">First name</label>
              <input v-model="staff.first_name" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">Last name</label>
              <input v-model="staff.last_name" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">Phone</label>
              <input v-model="staff.phone" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">Role</label>
              <input v-model="staff.role" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="table-wrapper">
      <h5 class="mt-2">User orders</h5>
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
import { ref, onMounted } from 'vue';
import { getUser, getOrders } from '@/services/api';
import { useRoute, useRouter } from 'vue-router';
import PaginationLayout from '@/components/layouts/PaginationLayout.vue'
// import { useAuthStore } from '@/stores/auth';
// const user = authStore.user;

const router = useRouter();
const route = useRoute();

const staff = ref({});
const orders = ref([]);

const currentPage = ref(1);
const totalPages = ref(1);

const fetchStaff = async () => {
  try{
  const id = route.params.id;
  const response = await getUser(id);

  staff.value = response.data
  } catch (error) {
    console.log(error);
  }
};

const fetchOrders = async () => {
  try {
    const response = await getOrders({
      page: currentPage.value,
      user_id: staff.value?.id
    });
    orders.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / 10);
  } catch (error) {
    console.error('Error:', error);
  }
};

const goToOrder = (id) => {
  router.push({ name: 'OrderDetail', params: { id } });
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
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
};
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
};

onMounted(async () => {
  await fetchStaff();
  await fetchOrders();
});
</script>

<style scoped>
.profile-image {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #637789;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 600;
  flex-shrink: 0;
}

.form-control:disabled {
  background-color: #e9ecef;
  opacity: 0.8;
}
</style>