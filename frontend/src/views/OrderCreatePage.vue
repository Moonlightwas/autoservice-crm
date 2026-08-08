<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="mb-0">Order create</h3>
    </div>

    <div class="d-flex justify-content-center">
      <div class="card p-4">
        <div class="flex-grow-1">
          <div v-if="isAdmin">
            <div class="col mb-3">
              <FormInput
                id="client"
                label="Client"
                type="text"
                v-model="clientId"
                :error-source="error"
              />
            </div>
            <div class="col mb-3">
              <label class="form-label">Source</label>
              <select class="form-control" v-model="source">
                <option value="manager">Manager</option>
                <option value="online">Online</option>
                <option value="phone">Phone</option>
              </select>
            </div>
          </div>
          <div class="col mb-3">
            <label class="form-label">Car</label>
            <select class="form-control" v-model="carId">
              <option
                v-for="car in userCars" 
                :key="car.id"
                :value="car.id"
              >
                {{ car.brand }} {{ car.model }} ({{ car.plate_number }})
              </option>
            </select>
            <router-link class="create-car-link" :to="{ name: 'CarCreate' }" @click="toggleSidebar">
              <i class="bi bi-plus"></i>Add new car
            </router-link>
          </div>
          <div class="col mb-3">
            <label class="form-label">Discribe your problem</label>
            <textarea
              v-model="description"
              class="form-control"
              placeholder="Type here"
            >
            </textarea>
          </div>
          <div class="col mb-3">
            <label class="form-label">Photo(optional)</label>
            <input
              type="file"
              accept="image/jpeg,image/png"
              class="form-control"
            >
          </div>
          
          <div class="control-buttons">
            <button class="btn btn-primary btn-sm ms-2" @click="saveOrder">Save</button>
            <button class="btn btn-secondary btn-sm ms-2" @click="cancelEdit">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import { getCars } from '@/services/api';
import { createOrder } from '@/services/api';
import FormInput from '@/components/FormInput.vue';

const router = useRouter();
const authStore = useAuthStore();

const user = authStore.user;
const userCars = ref([]);
const clientId = ref('');
const source = ref('');
// search params
const carId = ref('');
const description = ref('');

const error = ref('');

const isAdmin = computed(() => {
  return ['manager', 'admin'].includes(user.role);
});

const cancelEdit = () => {
  router.back();
};

const getUserCars = async () => {
  const response = await getCars();
  userCars.value = response.data.results;
};

const saveOrder = async () => {
  try {
    const params = {};
    if (isAdmin.value) {
      params.source = source.value;
      params.client = clientId.value;
      params.car = carId.value;
      params.description = description.value;
    } else {
      params.client = user.id;
      params.car = carId.value;
      params.description = description.value;
    }

    await createOrder(params);

    router.push({name: 'Orders'})
  } catch (err) {
    if (err.response) {
      error.value = err.response.data;
    }
  }
};

onMounted(() => {
  getUserCars();
});
</script>

<style scoped>
.card {
  width: 70%;
}
.create-car-link {
  text-decoration: none;
}
.nav-link:hover {
  text-decoration: none;
}

.card textarea {
  overflow: hidden;
  max-height: 1500px;
  height: auto;
  resize: none;
}
.control-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
</style>