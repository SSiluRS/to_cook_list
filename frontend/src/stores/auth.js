import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    username: localStorage.getItem('username') || null,
    error: null,
    loading: false
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  
  actions: {
    async register(username, email, password) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/api/v1/auth/register', { username, email, password })
        const { access_token } = response.data
        this.token = access_token
        this.username = username
        
        localStorage.setItem('token', access_token)
        localStorage.setItem('username', username)
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Registration failed'
        return false
      } finally {
        this.loading = false
      }
    },
    
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/api/v1/auth/login', { username, password })
        const { access_token } = response.data
        this.token = access_token
        this.username = username
        
        localStorage.setItem('token', access_token)
        localStorage.setItem('username', username)
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Invalid username or password'
        return false
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      this.token = null
      this.username = null
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  }
})
