<template>
  <div class="container mt-2 pt-3">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card" style="border: none;">
          <div class="card-body">
            <div v-if="isSuccess" class="alert alert-success text-center py-4 mt-3">
              <h5 class="alert-heading mb-1">{{ successMessage }}</h5>
            </div>

            <form @submit.prevent="handleRegister" novalidate>
              <FormInput
                id="email"
                label="Email:"
                type="email"
                v-model="email"
                :error-source="error"
              />

              <FormInput
                id="first_name"
                label="First name:"
                type="text"
                v-model="first_name"
                :error-source="error"
              />

              <FormInput
                id="last_name"
                label="Last name:"
                type="text"
                v-model="last_name"
                :error-source="error"
              />

              <FormInput
                id="phone"
                label="Phone:"
                type="text"
                v-model="tel"
                :error-source="error"
              />

              <FormInput
                id="password"
                label="Password:"
                type="password"
                v-model="password"
                :error-source="error"
              />

              <FormInput
                id="password_confirm"
                label="Password confirm:"
                type="password"
                v-model="password_confirm"
                :error-source="error"
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
import { register } from '@/services/api';

export default {
  components: {
    FormInput
  },

  data() {
    return {
        email: '',
        password: '',
        password_confirm: '',
        first_name: '',
        last_name: '',
        phone: '',
        error: '',
        isSuccess: false,
        successMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      this.error = '';
      this.successMessage = null;

      try {
        const response = await register(
          this.email,
          this.password,
          this.password_confirm,
          this.first_name,
          this.last_name,
          this.phone
        );

        this.isSuccess = true;
        this.successMessage = response.data.message;

        setTimeout(() => {
          this.$router.push({ name: 'Login' });
        }, 1500);
      }
      catch (err) {
        if (err.response) {
          this.error = err.response.data
        } else {
          this.error = 'Unknown error'
        }
      }
    }
  }
}
</script>