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
              <FormSelect
                id="client"
                label="Client"
                v-model="clientId"
                option-type="user"
                :options="clients"
                :reduce="option => option.id"
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
            <div v-if="error?.source" class="invalid-feedback d-block">
              {{ error.source[0] }}
            </div>
          </div>

          <div class="col mb-3">
            <FormSelect
              id="car"
              label="Car"
              v-model="carId"
              option-type="car"
              :options="userCars"
              :error-source="error"
            />
            <router-link class="create-car-link" :to="{ name: 'CarCreate' }" @click="toggleSidebar">
              <i class="bi bi-plus"></i>Add new car
            </router-link>
          </div>

          <div class="col mb-3">
            <FormInput
              id="description"
              type="textarea"
              label="Discribe your problem"
              rows="4"
              v-model="description"
              placeholder="Type here"
              :error-source="error"
            />
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
            <button class="btn btn-primary btn-sm ms-2" @click="saveOrder">Create</button>
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
import { createOrder, getUsers } from '@/services/api';
import FormSelect from '@/components/FormSelect.vue';
import FormInput from '@/components/FormInput.vue';

const router = useRouter();
const authStore = useAuthStore();

const user = authStore.user;
const clients = ref([]);
const userCars = ref([]);
const clientId = ref('');
const source = ref(null);
// save request body params
const carId = ref('');
const description = ref('');

const error = ref('');

const isAdmin = computed(() => {
  return user && ['manager', 'admin'].includes(user.role);
});

const cancelEdit = () => {
  router.back();
};

const getClients = async () => {
  const response = await getUsers();
  clients.value = response.data.results;
}

const getUserCars = async () => {
  const response = await getCars();
  userCars.value = response.data.results;
};

const saveOrder = async () => {
  try {
    const params = {};
    params.source = isAdmin.value ? source.value : 'online';
    params.client = isAdmin.value ? clientId.value : user.id;
    params.car = carId.value;
    params.description = description.value;

    await createOrder(params);

    router.push({name: 'Orders'})
  } catch (err) {
    if (err.response) {
      error.value = err.response.data;
    }
  }
};

onMounted(() => {
  if (isAdmin.value) getClients();
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

.control-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
</style>