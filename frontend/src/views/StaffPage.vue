<template>
  <div class="page">
    <h3>Staff</h3>

    <div class="search input-group rounded w-5">
      <input
        type="search"
        class="form-control"
        placeholder="Search"
        aria-label="Search"
        aria-describedby="search-addon"
        v-model="search"
        @keydown.enter="handleSearch"
      />
      <select
        name="form-select"
        style="border: 1px solid lightgray;"
        v-model="role"
        @change="handleSearch"
      >
        <option value="">All roles</option>
        <option value="client">Client</option>
        <option value="mechanic">Mechanic</option>
        <option value="manager">Manager</option>
        <option value="admin">Admin</option>
      </select>
      <button class="btn btn-primary" @click="handleSearch">
        <i class="bi bi-search"></i>
      </button>
  </div>

    <div class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>user orders</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="employee in staff"
            :key="employee.id"
            @click="goToUser(employee.id)"
            style="cursor: pointer;"
          >
            <td>{{ employee.id }}</td>
            <td>
              <div class="d-flex align-items-center gap-2">
                <div class="profile-image">
                  {{ employee.email[0].toUpperCase() || 'U' }}
                </div>
                <span>{{ (employee.first_name + ' ' + employee.last_name).trim() || '—'  }}</span>
              </div>
            </td>
            <td>{{ employee.email }}</td>
            <td>{{ employee.role }}</td>
            <td>{{ employee.orders_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationLayout 
      :current-page="currentPage"
      :total-pages="totalPages"
      @page-change="(page) => { currentPage = page; fetchStaff() }"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getUsers } from '@/services/api';
import PaginationLayout from '@/components/layouts/PaginationLayout.vue'
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const staff = ref([]);
const currentPage = ref(1)
const totalPages = ref(1)
//  search params
const role = ref('');
const search = ref('');

const fetchStaff = async () => {
  try {
    const params = { page: currentPage.value }
    if (role.value)  params.role = role.value;
    if (search.value) params.search = search.value;
    
    await router.replace({
    query: { 
      page: currentPage.value,
      role: role.value || undefined,
      search: search.value || undefined
    }});

    const response = await getUsers(params);

    staff.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / 10);
  } catch (error) {
    console.error('Error:', error);
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchStaff();
};

const goToUser = (id) => {
  router.push({ name: 'StaffDetail', params: { id } });
};

onMounted(() => {
  const query = route.query;
  if (query.page) currentPage.value = parseInt(query.page);
  if (query.role) role.value = query.role;
  if (query.search) search.value = query.search;

  fetchStaff();
});
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
}

.table-wrapper {
  flex: 1;
}
.table tbody tr td {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 5px;
}
.table tbody tr:hover td {
  cursor: pointer;
  background-color: #f0f7ff;
  transition: background-color 0.3s ease;
}
.table span.baged {
  padding: 2px 8px;
  font-weight: 600;
  border: 0px solid;
  border-radius: 5px;
}
.table .profile-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #637789;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}
</style>