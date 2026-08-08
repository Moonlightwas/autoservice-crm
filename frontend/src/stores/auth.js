import { defineStore } from "pinia";
import { 
    login as apiLogin,
    logout as apiLogout,
    profile as apiProfile,
    setAccessToken,
    getAccessToken 
} from '@/services/api';

let initPromise = null;

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isInitialized: false
    }),
    
    actions: {
      async init() {
        if (this.isInitialized) return;
        
        if (initPromise) return initPromise;
        
        initPromise = (async () => {
          try {
            const { data: userData } = await apiProfile();
            this.user = userData;
          }
          catch (error) {
            this.user = null;
            setAccessToken(null);
          }
          finally {
            this.isInitialized = true;
          }
        })();

        return initPromise;
      },

      async login(credentials) {
        try{
          const { data } = await apiLogin(credentials.email, credentials.password);
          setAccessToken(data.access);

          const { data: userData } = await apiProfile();
          this.user = userData;
          this.isInitialized = true;
        } catch (error) {
          setAccessToken(null);
          throw error;
        }
      },
        
      async logout() {
        try {
          if (getAccessToken()) {
            await apiLogout();
          }
        } catch (error) {
          console.warn('Logout API error:', error);
        } finally {
          this.user = null;
          setAccessToken(null);
          this.isInitialized = true;
        }
      }
    },

    getters: {
      isAuthenticated: (state) => !!state.user && !!getAccessToken()
    }
})