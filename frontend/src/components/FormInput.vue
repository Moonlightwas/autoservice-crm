<template>
  <label :for="id" class="form-label">{{ label }}</label>
  <textarea
    v-if="type === 'textarea'"
    :id="id"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    :class="['form-control', { 'is-invalid': hasError }]"
    :placeholder="placeholder"
    v-bind="$attrs"
  ></textarea>
  
  <div v-else class="input-group">
    <input
      :id="id"
      :type="inputType"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :class="['form-control', { 'is-invalid': hasError }]"
      v-bind="$attrs"
    />

    <button
      v-if="type === 'password'"
      class="btn"
      type="button"
      @click="toggleVisibility"
    >
    
      <i :class="isVisible ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
    </button>
  </div>

  <div v-if="hasError" class="invalid-feedback d-block">
    {{ errorMessage }}
  </div>
</template>

<script>
export default {
  name: 'FormInput',
  props: {
    id: String,
    label: String,
    type: {
      type: String,
      default: 'text'
    },
    modelValue: {
      type: String,
      default: ''
    },
    errorSource: {
      type: [Object, String, null],
      default: null
    },
    showPassword: {
      type: Boolean,
      default: false
    }
  },

  emits: ['update:showPassword'],

  computed: {
    isVisible: {
      get() { return this.showPassword },
      set(value) { return this.$emit('update:showPassword', value) }
    },
    inputType() {
      if (this.type === 'password' && this.isVisible) {
        return 'text';
      }
      return this.type;
    },

    hasError() {
      return !!(this.errorSource && this.errorSource[this.id]);
    },
    errorMessage() {
      if (!this.hasError) return '';
      const fieldError = this.errorSource[this.id];
      return Array.isArray(fieldError) ? fieldError.join(', ') : fieldError;
    }
  },
  
  methods: {
    toggleVisibility() {
      this.isVisible = !this.isVisible;
    }
  }
}
</script>

<style>
textarea {
  height: auto;
  resize: none;
}
</style>