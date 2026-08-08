<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="mb-0">Car create</h3>
    </div>

    <div class="d-flex justify-content-center">
      <div class="card p-4">
        <div class="flex-grow-1">
          <div v-if="isAdmin">
            <div class="col mb-3">
              <v-select
                v-model="carOwnerId"
                :options="owners"
                :reduce="owner => owner.id"
                label="email"
                placeholder="Search by email, phone or name..."
                :class="{ 'is-invalid': error?.owner }"
              >
                <template #option="{ email, first_name, last_name, id }">
                  <div class="owner-option">
                    <span class="owner-email">{{ email }}</span>
                    <span v-if="first_name || last_name" class="owner-name">
                      ({{ first_name }} {{ last_name }})
                    </span>
                    <span class="owner-id">#{{ id }}</span>
                  </div>
                </template>
              </v-select>
            </div>
          </div>
          <div class="col mb-3">
            <FormInput
              id="brand"
              label="Brand"
              type="text"
              v-model="carBrand"
              :error-source="error"
            />
          </div>
          <div class="col mb-3">
            <FormInput
              id="model"
              label="Model"
              type="text"
              v-model="carModel"
              :error-source="error"
            />
          </div>
          <div class="col mb-3">
            <FormInput
              id="year"
              label="Year"
              type="number"
              v-model="carYear"
              :error-source="error"
              min="1900"
              max="2100"
            />
          </div>
          <div class="col mb-3">
            <FormInput
              id="vin"
              label="VIN"
              type="text"
              v-model="carVIN"
              :error-source="error"
            />
          </div>
          <div class="col mb-3">
            <FormInput
              id="plate_number"
              label="Plate number"
              type="text"
              v-model="carPlateNumber"
              :error-source="error"
            />
          </div>
          
          <div class="control-buttons">
            <button class="btn btn-primary btn-sm ms-2" @click="handleCreateCar">Save</button>
            <button class="btn btn-secondary btn-sm ms-2" @click="cancelEdit">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { ref, computed } from 'vue';
import { createCar } from '@/services/api';
import FormInput from '@/components/FormInput.vue';
import 'vue-select/dist/vue-select.css';


const router = useRouter();
const authStore = useAuthStore();

const user = authStore.user;

const error = ref('');

const carOwnerId = ref('');
const carBrand = ref('');
const carModel = ref('');
const carYear = ref('');
const carVIN = ref('');
const carPlateNumber = ref('');

const isAdmin = computed(() => {
  return ['manager', 'admin'].includes(user.role);
});

const cancelEdit = () => {
  router.back();
};

const handleCreateCar = async () => {
  error.value = '';

  try {
    carOwnerId.value = isAdmin.value ? carOwnerId.value : user.id;
    await createCar(
      carOwnerId.value,
      carBrand.value,
      carModel.value,
      carYear.value,
      carVIN.value,
      carPlateNumber.value
    );

    router.back();
  } catch (err) {
    if (err.response) {
      error.value = err.response.data;
    }
  }
};
</script>

<style scoped>
@import "vue-select/dist/vue-select.css";

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