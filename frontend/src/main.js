import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import VueSelect from 'vue-select'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.component("v-select", VueSelect)
app.mount('#app')
