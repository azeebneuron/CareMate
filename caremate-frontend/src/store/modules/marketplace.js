// src/store/modules/marketplace.js
import api from '@/api/axios'

export default {
  namespaced: true,

  state: () => ({
    caregivers: [],
    loading: false,
    error: null,
    userProfile: null, // For caregivers managing their own profile
    caregiverProfile: null,
    profileStats: {
        totalReviews: 0,
        averageRating: 0,
        profileViews: 0
    }
  }),

  mutations: {
    SET_CAREGIVERS(state, caregivers) {
      state.caregivers = caregivers
    },
    SET_USER_PROFILE(state, profile) {
      state.userProfile = profile
    },
    ADD_REVIEW(state, { caregiverId, review }) {
      const caregiver = state.caregivers.find(c => c.id === parseInt(caregiverId))
      if (caregiver) {
        caregiver.reviews.push(review)
      }
    },
    UPDATE_PROFILE(state, profile) {
      state.userProfile = profile
      // Also update in caregivers list if present
      const index = state.caregivers.findIndex(c => c.id === profile.id)
      if (index !== -1) {
        state.caregivers[index] = { ...state.caregivers[index], ...profile }
      }
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_CAREGIVER_PROFILE(state, profile) {
        state.caregiverProfile = profile
      },
    SET_PROFILE_STATS(state, stats) {
        state.profileStats = stats
      }
  },

  actions: {
    async fetchCaregivers({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/caregivers/search')
        commit('SET_CAREGIVERS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async fetchUserProfile({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/caregivers/profile')
        commit('SET_USER_PROFILE', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async createProfile({ commit }, profileData) {
      try {
        const response = await api.post('/caregivers/profile', profileData)
        commit('SET_USER_PROFILE', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async updateProfile({ commit }, profileData) {
      try {
        const response = await api.put('/caregivers/profile', profileData)
        commit('UPDATE_PROFILE', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async addReview({ commit }, { caregiverId, rating, comment }) {
      try {
        const response = await api.post(`/caregivers/${caregiverId}/reviews`, {
          rating,
          comment
        })
        commit('ADD_REVIEW', {
          caregiverId,
          review: response.data
        })
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async contactCaregiver({ commit }, { caregiverId, message, preferredTime }) {
      try {
        const response = await api.post(`/caregivers/${caregiverId}/contact`, {
          message,
          preferred_time: preferredTime
        })
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },
    async fetchCaregiverProfile({ commit }) {
        try {
          const response = await api.get('/caregivers/profile')
          commit('SET_CAREGIVER_PROFILE', response.data)
          return response.data
        } catch (error) {
          commit('SET_ERROR', error.message)
          throw error
        }
      },
      async updateCaregiverProfile({ commit }, profileData) {
        try {
          const response = await api.put('/caregivers/profile', profileData)
          commit('SET_CAREGIVER_PROFILE', response.data)
          return response.data
        } catch (error) {
          commit('SET_ERROR', error.message)
          throw error
        }
      },
      async fetchProfileStats({ commit }) {
        try {
          const response = await api.get('/caregivers/profile/stats')
          commit('SET_PROFILE_STATS', response.data)
          return response.data
        } catch (error) {
          commit('SET_ERROR', error.message)
          throw error
        }
      }
  },

  getters: {
    isCaregiver: (state, getters, rootState) => {
      return rootState.auth.userType === 'caregiver'
    },
    topCaregivers: (state) => {
      return [...state.caregivers]
        .sort((a, b) => b.average_rating - a.average_rating)
        .slice(0, 5)
    },
    isCaregiverProfileComplete: (state) => {
        if (!state.caregiverProfile) return false
        const required = [
          'hourly_rate',
          'experience_years',
          'specializations',
          'bio'
        ]
        return required.every(field => 
          state.caregiverProfile[field] && 
          state.caregiverProfile[field].length > 0
        )
      }
  }
}