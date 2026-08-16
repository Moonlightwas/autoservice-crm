import axios from 'axios'
import { applyAuthTokenInterceptor } from 'axios-auth-refresh-queue'; 

const api = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    timeout: process.env.VUE_APP_API_TIMEOUT,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true
});

let accessToken = null;

export function setAccessToken(token) {
  accessToken = token;
}

export function getAccessToken() {
  return accessToken;
}

applyAuthTokenInterceptor(api, {
  headerTokenHandler: (config) => {
    if (accessToken) {
      config.headers.set('Authorization', `Bearer ${accessToken}`);
    }
  },

  requestRefresh: async () => {
    const response = await axios.post(
      `${process.env.VUE_APP_API_URL}auth/token/refresh/`,
      {},
      {withCredentials: true}
    );

    return {
      accessToken: response.data.access
    }
  },

  onSuccess: (newTokens) => {
    setAccessToken(newTokens.accessToken);
  },

  onFailure: () => {
    setAccessToken(null);
  },
  
  shouldIntercept: (config) => {
    return !config.url?.includes('/auth/token/refresh/');
  },

  crossTabSync: true,
  debug: false
})

export const register = (email, password, password_confirm, first_name, last_name, phone) => {
    return api.post('auth/register/', {
      email,
      password,
      password_confirm,
      first_name,
      last_name,
      phone
    })
}

export const login = (email, password) => {
    return api.post('auth/login/', {email, password})
}

export const refresh = () => {
    return axios.post(`${process.env.VUE_APP_API_URL}auth/token/refresh/`, {}, { withCredentials: true })
}

export const logout = () => {
    return api.post('auth/logout/')
}

export const profile = () => {
    return api.get('users/profile/')
}

export const updateProfile = (email, first_name, last_name, phone) => {
    return api.patch('users/profile/', {email, first_name, last_name, phone})
}

export const getOrders = (params) => {
  return api.get('orders/', {params})
}

export const getOrder = (id) => {
  return api.get(`orders/${id}/`)
}

export const createOrder = (params) => {
  return api.post('orders/', params)
}

export const forceStatus = (id, params) => {
  return api.patch(`orders/${id}/force-status/`, params)
}

export const getUsers = (params) => {
  return api.get('users/', {params})
}

export const getUser = (id) => {
  return api.get(`users/${id}/`)
}

export const getCars = (params) => {
  return api.get('cars/', {params})
}

export const getCar = (id) => {
  return api.get(`cars/${id}`)
}

export const createCar = (params) => {
  return api.post('cars/', params)
}

export default api;