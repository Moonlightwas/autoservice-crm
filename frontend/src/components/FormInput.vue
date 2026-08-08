<template>
  <div class="mb-3">
    <label :for="id" class="form-label">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :class="['form-control', { 'is-invalid': hasError }]"
      v-bind="$attrs"
    />
    <div v-if="hasError" class="invalid-feedback">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'FormInput',
  props: {
    id: String,
    label: String,
    type: { type: String, default: 'text' },
    modelValue: String,
    errorSource: [Object, String, null]
  },
  computed: {
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