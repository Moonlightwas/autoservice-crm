<template>
  <div class="page">
    <div class="d-flex justify-content-between ">
      <h3>Cars</h3>

      <div v-if="!isMechanic" class="order-buttons">
        <RouterLink :to="{ name: 'CarCreate' }">
          <button class="btn btn-primary btn-sm">Create car</button>
        </RouterLink>
      </div>
    </div>

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
      <button class="btn btn-primary" @click="handleSearch">
        <i class="bi bi-search"></i>
      </button>
  </div>

    <div class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Brand</th>
            <th>Model</th>
            <th>Year</th>
            <th>Vin</th>
            <th>Plate number</th>
            <th>Owner</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="car in cars"
            :key="car.id"
            @click="goToCar(car.id)"
            style="cursor: pointer;"
          >
            <td>{{ car.id }}</td>
            <td>{{ car.brand }}</td>
            <td>{{ car.model }}</td>
            <td>{{ car.year }}</td>
            <td>{{ car.vin }}</td>
            <td>{{ car.plate_number }}</td>
            <td>{{ car.owner.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationLayout 
      :current-page="currentPage"
      :total-pages="totalPages"
      @page-change="(page) => { currentPage = page; fetchCars() }"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getCars } from '@/services/api';
import PaginationLayout from '@/components/layouts/PaginationLayout.vue'
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const cars = ref([]);
const currentPage = ref(1)
const totalPages = ref(1)
//  search params
const search = ref('');

const fetchCars = async () => {
  try {
    const params = { page: currentPage.value }
    if (search.value) params.search = search.value;
    
    await router.replace({
    query: { 
      page: currentPage.value,
      search: search.value || undefined
    }});

    const response = await getCars(params);

    cars.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / 10);
  } catch (error) {
    console.error('Error:', error);
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchCars();
};

const goToCar = (id) => {
  router.push({ name: 'CarDetail', params: { id } });
};


onMounted(() => {
  const query = route.query;
  if (query.page) currentPage.value = parseInt(query.page);
  if (query.search) search.value = query.search;

  fetchCars();
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