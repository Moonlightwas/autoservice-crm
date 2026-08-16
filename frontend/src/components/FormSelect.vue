<template>
  <label :for="id" class="form-label">{{ label }}</label>
  <v-select
    :id="id"
    v-model="selectedValue"
    :options="options"
    :reduce="option => option.id"
    :class="{ 'is-invalid': hasError }"
    :filter-by="customFilter"
    :get-option-label="getOptionLabel"
  >
    <template #option="{ id, email, phone, first_name, last_name, 
      brand, model, vin, plate_number, label }"
    >
      <div v-if="optionType === 'user'">
        <span>#{{ id }} {{ email }} {{ phone }} {{ first_name }} {{ last_name }}</span>
      </div>

      <div v-else-if="optionType === 'car'">
        <span>{{ vin }} {{ plate_number }} {{ brand }} {{ model }}</span>
      </div>

      <div v-else>
        {{ label }}
      </div>
    </template>

    <template #selected-option="{ id, email, phone, first_name, last_name, 
      brand, model, vin, plate_number, label }">
      <div v-if="optionType === 'user'">
        <span>#{{ id }} {{ email }} {{ phone }} {{ first_name }} {{ last_name }}</span>
      </div>

      <div v-else-if="optionType === 'car'">
        <span>{{ vin }} {{ plate_number }} {{ brand }} {{ model }}</span>
      </div>

      <div v-else>
        {{ label }}
      </div>
    </template>
  </v-select>

  <div v-if="hasError" class="invalid-feedback d-block">
    {{ errorMessage }}
  </div>
</template>

<script>
export default {
  name: 'FormSelect',
  props: {
    id: String,
    label: String,
    modelValue: {
      type: [String, Number],
      default: ''
    },
    optionType: {
      type: String,
      default: ''
    },
    options: Array,
    errorSource: {
      type: [Object, String, null],
      default: null
    }
  },

  emits: ['update:modelValue'],

  methods: {
    customFilter(option, label, search) {
      if (!option) return false;
      if (!search || search.trim() === '') return true;

      const searchLower = search.toLowerCase().trim();
      
      const searchableFields = [
        option.id ? `#${option.id}` : '',
        option.id ? String(option.id) : '',
        option.email,
        option.first_name,
        option.last_name,
        option.phone,
        option.brand,
        option.model,
        option.plate_number,
        option.vin,
        label
      ];

      const searchableText = searchableFields
        .filter(field => field !== null && field !== undefined)
        .map(field => String(field).toLowerCase())
        .join(' ');

      return searchableText.includes(searchLower);
    },

    getOptionLabel(option) {
      if (!option) return '';
      if (this.optionType === 'user') {
        return `${option.first_name || ''} ${option.last_name || ''} ${option.email || ''}`.trim();
      }
      if (this.optionType === 'car') {
        return `${option.brand || ''} ${option.model || ''} ${option.plate_number || ''}`.trim();
      }
      return option.label || '';
    }
  },

  computed: {
    selectedValue: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    },

    hasError() {
      return !!(this.errorSource && this.errorSource[this.id]);
    },
    errorMessage() {
      if (!this.hasError) return '';
      const fieldError = this.errorSource[this.id];
      return Array.isArray(fieldError) ? fieldError.join(', ') : fieldError;
    }
  }
}
</script>