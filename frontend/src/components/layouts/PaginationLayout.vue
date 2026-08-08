<template>
  <div class="pagination-wrapper">
    <nav aria-label="Page navigation">
      <ul class="pagination">
        <li class="page-item">
          <a class="page-link" href="#" aria-label="Previous" @click.prevent="pageChange(currentPage - 1)">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li
          v-for="page in visiblePages"
          :key="page"
          class="page-item"
          :class="{ active: currentPage === page }"
        >
          <a class="page-link" href="#" @click.prevent="emit('page-change', page)">
            {{ page }}
          </a>
        </li>
        <li class="page-item">
          <a class="page-link" href="#" aria-label="Next" @click.prevent="pageChange(currentPage + 1)">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';
const props = defineProps({
  currentPage: Number,
  totalPages: Number
})
const emit = defineEmits(['page-change']);

const pageChange = (page) => {
  if (page < 1 || page > props.totalPages) return;
  emit('page-change', page);
};

const visiblePages = computed(() => {
  const maxVisible = 3;

  let start = props.currentPage - Math.ceil(maxVisible / 2);
  let end = props.currentPage + Math.ceil(maxVisible / 2);

  if (start < 1) { start = 1; end = maxVisible; }
  if (end > props.totalPages) { end = props.totalPages; start = end - maxVisible; }

  return Array.from({ length: props.totalPages }, (_, i) => i + 1).slice(start-1, end);
})
</script>

<style scoped>
.pagination-wrapper {
  display: flex;
  justify-content: center;
}
</style>