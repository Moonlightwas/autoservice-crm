<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="mb-0">Profile</h3>
    </div>

    <div class="card p-4">
      <div class="d-flex align-items-start gap-4">
        <div class="profile-image">
          {{ user.email?.[0].toUpperCase() || '?' }}
        </div>

        <div class="flex-grow-1">
          <div class="row g-2">
            <div class="col-md-6">
              <label class="form-label">Email</label>
              <input v-model="user.email" type="text" class="form-control form-control-sm" :disabled="!isEditing">
            </div>
            <div class="col-md-6">
              <label class="form-label">First name</label>
              <input v-model="user.first_name" type="text" class="form-control form-control-sm" :disabled="!isEditing">
            </div>
            <div class="col-md-6">
              <label class="form-label">Last name</label>
              <input v-model="user.last_name" type="text" class="form-control form-control-sm" :disabled="!isEditing">
            </div>
            <div class="col-md-6">
              <label class="form-label">Phone</label>
              <input v-model="user.phone" type="text" class="form-control form-control-sm" :disabled="!isEditing">
            </div>
          </div>
          
          <div class="control-buttons">
            <div v-if="isEditing">
              <button class="btn btn-primary btn-sm" @click="saveProfile">Save</button>
              <button class="btn btn-secondary btn-sm ms-2" @click="cancelEdit">Cancel</button>
            </div>
            <div v-else>
              <button class="btn btn-primary btn-sm" @click="toggleEdit">Edit</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { updateProfile } from '@/services/api';

const authStore = useAuthStore();
const user = authStore.user;

const originalUserData = ref({ ...user });
const isEditing = ref(false);

const toggleEdit = () => {
  if (isEditing.value) {
    cancelEdit();
  } else {
    isEditing.value = true;
  }
};

const cancelEdit = () => {
  isEditing.value = false;
  Object.assign(user, originalUserData.value);
};

const saveProfile = async () => {
  try {
    await updateProfile(
      user.email,
      user.first_name,
      user.last_name,
      user.phone
    );
    originalUserData.value = { ...user };
    isEditing.value = false;
  } catch {
    alert('Failed to update profile.');
    Object.assign(user, originalUserData.value);
  }
};
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