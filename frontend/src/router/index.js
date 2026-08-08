import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NotFound from '@/views/NotFound.vue'
import RegisterPage from '@/views/auth/RegisterPage.vue'
import LoginPage from '@/views/auth/LoginPage.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import DashboardPage from '@/views/DashboardPage.vue'
import OrdersPage from '@/views/OrdersPage.vue'
import OrderDetailPage from '@/views/OrderDetailPage.vue'
import OrderCreatePage from '@/views/OrderCreatePage.vue'
import CarsPage from '@/views/CarsPage.vue'
import CarCreate from '@/views/CarCreate.vue'
import CarDetail from '@/views/CarDetail.vue'
import StaffPage from '@/views/StaffPage.vue'
import StaffDetail from '@/views/StaffDetail.vue'
import HomeLayout from '@/components/layouts/HomeLayout.vue'



const routes = [
  // public
  {
    path: '/',name: "Home",
    component: HomeLayout,
    meta: {title: 'Home'}
  },

  // auth
  {
    path: '/register',
    name: "Register",
    component: RegisterPage,
    meta: {title: 'Sign Up'}
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: {title: 'Sign In'}
  },
  {
    path: '/logout',
    name: 'Logout',
    beforeEnter: async (to, from, next) => {
      const authStore = useAuthStore()
      await authStore.logout()
      next({ name: 'Home' })
    }
  },

  // Pages that requires auth
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: {title: 'Dashboard', requiresAuth: true}
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
    meta: {title: 'Profile', requiresAuth: true}
  },

  // Orders pages
  {
    path: '/orders',
    name: 'Orders',
    component: OrdersPage,
    meta: {title: 'Orders', requiresAuth: true}
  },
  {
    path: '/orders/:id',
    name: 'OrderDetail',
    component: OrderDetailPage,
    meta: {title: 'Orders', requiresAuth: true}
  },
  {
    path: '/orders/create',
    name: 'OrderCreate',
    component: OrderCreatePage,
    meta: {title: 'Orders', requiresAuth: true}
  },

  // Car pages
  {
    path: '/cars',
    name: 'Cars',
    component: CarsPage,
    meta: {title: 'Cars', requiresAuth: true}
  },
  {
    path: '/cars/:id',
    name: 'CarDetail',
    component: CarDetail,
    meta: {title: 'Cars', requiresAuth: true}
  },
  {
    path: '/cars/create',
    name: 'CarCreate',
    component: CarCreate,
    meta: {title: 'Cars', requiresAuth: true}
  },

  {
    path: '/staff',
    name: 'Staff',
    component: StaffPage,
    meta: {title: 'Staff', requiresAuth: true}
  },
  {
    path: '/staff/:id',
    name: 'StaffDetail',
    component: StaffDetail,
    meta: {title: 'Staff', requiresAuth: true}
  },

  // Not found
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {title: 'Not Found'}
  }
]

const router = createRouter({
  history: createWebHistory(),
  linkActiveClass: 'active',
  routes
})

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title
  
  const authStore = useAuthStore();

  await authStore.init();

  if (to.meta?.requiresAuth){
    if (!authStore.isAuthenticated) {
      return next({ 
        name: 'Login', 
        query: { redirect: to.fullPath } 
      })
    }
    return next()
  }

  if ((to.name === 'Login' || to.name === 'Register') && authStore.isAuthenticated) {
    return next({ name: 'Profile' });
  }

  next();
})

export default router