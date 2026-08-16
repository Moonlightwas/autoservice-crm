<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="mb-0">Car detail</h3>
    </div>

    <div class="card p-4">
      <div class="d-flex align-items-start gap-4">
        <div class="flex-grow-1">
          <div class="row g-2">
            <div class="col-md-6">
              <label class="form-label">Brand</label>
              <input v-model="car.brand" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">Model</label>
              <input v-model="car.model" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">Year</label>
              <input v-model="car.year" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">VIN</label>
              <input v-model="car.vin" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
            <div class="col-md-6">
              <label class="form-label">Plate number</label>
              <input v-model="car.plate_number" type="text" class="form-control form-control-sm" :disabled="true">
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="table-wrapper">
      <h5 class="mt-2">Repair history</h5>
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Status</th>
            <th>Description</th>
            <th>Created at</th>
            <th>Mechanics</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="order in car.orders"
            :key="order.id"
            @click="goToOrder(order.id)"
            style="cursor: pointer;"
          >
          <td>{{ order.id }}</td>
          <td>
            <span class="baged" :class="getStatusClass(order.status)">
              {{ getStatusLabel(order.status) }}
            </span>
          </td>
          <td>{{ order.description }}</td>
          <td>{{ formatDate(order.created_at) }}</td>
          <td>
            <div v-for="mechanic in order.mechanic" :key="mechanic.id">
              {{ mechanic }}
            </div>
          </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getCar } from '@/services/api';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();

const car = ref({});

const fetchCar = async () => {
  const id = useRoute().params.id;
  try {
    const response = await getCar(id);
    car.value = response.data;
  } catch (error) {
    console.error('Error:', error);
  }
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

const goToOrder = (id) => {
  router.push({ name: 'OrderDetail', params: { id } });
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

onMounted(fetchCar);
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

.control-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
</style>