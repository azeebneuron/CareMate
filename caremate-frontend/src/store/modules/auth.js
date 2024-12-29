// src/store/modules/auth.js
import api from '@/api/axios'

export default {
  namespaced: true,
  
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    userType: localStorage.getItem('userType'),
    loading: false,
    error: null
  }),
  
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    SET_USER_TYPE(state, type) {
      state.userType = type
      if (type) {
        localStorage.setItem('userType', type)
      } else {
        localStorage.removeItem('userType')
      }
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async login({ commit }, credentials) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const response = await api.post('/auth/login', credentials)
        const { user, token } = response.data
        
        commit('SET_USER', user)
        commit('SET_TOKEN', token)
        commit('SET_USER_TYPE', user.user_type)
        
        return user
      } catch (error) {
        const errorMessage = error.response?.data?.message || 'Login failed'
        commit('SET_ERROR', errorMessage)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async register({ commit }, userData) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const response = await api.post('/auth/register', userData)
        return response.data
      } catch (error) {
        const errorMessage = error.response?.data?.message || 'Registration failed'
        commit('SET_ERROR', errorMessage)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async logout({ commit }) {
      commit('SET_USER', null)
      commit('SET_TOKEN', null)
      commit('SET_USER_TYPE', null)
    }
  },
  
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user,
    userType: state => state.userType,
    authError: state => state.error
  }
}