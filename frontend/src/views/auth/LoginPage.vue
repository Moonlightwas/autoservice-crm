<template>
  <div class="container mt-5 pt-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card" style="border: none">
          <div class="card-body">

            <form @submit.prevent="handleLogin" novalidate>
              <FormInput
                id="email"
                label="Email:"
                type="email"
                v-model="email"
                :error-source="error"
              />
              
              <FormInput
                id="password"
                label="Password:"
                type="password"
                v-model="password"
                :error-source="error"
                v-model:show-password="showPassword"
              />
              
              <button type="submit" class="btn btn-primary w-100">Sign In</button>
            </form>

            <div v-if="GeneralError" class="alert alert-danger mt-3">
              {{ GeneralError }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FormInput from '@/components/FormInput.vue';
import { useAuthStore } from '@/stores/auth';

export default {
  components: {
    FormInput
  },

  data() {
    return {
      email: '',
      password: '',
      error: null,
      showPassword: false
    }
  },

  computed: {
    GeneralError() {
      if (!this.error) return false;

      if (typeof this.error === 'string') {
        return this.error
      }

      if (this.error.detail) {
        return Array.isArray(this.error.detail) 
          ? this.error.detail.join(', ') 
          : this.error.detail;
      }
      
      return null;
    },
  },

  methods: {
    async handleLogin() {
      this.error = null;

      try {
        const authStore = useAuthStore();
        await authStore.login({
          email: this.email,
          password: this.password
        });
        
        const redirect = this.$route.query.redirect || '/';
        this.$router.push(redirect);
      }
      catch (err) {
        if (err.response) {
          this.error = err.response.data
        } else {
          this.error = 'Unknown error.'
        }
      }
    }
  }
}
</script>