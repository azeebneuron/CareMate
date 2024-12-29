// src/store/modules/health.js
import api from '@/api/axios'

export default {
  namespaced: true,
  
  state: () => ({
    metrics: [],
    loading: false,
    error: null
  }),
  
  mutations: {
    SET_METRICS(state, metrics) {
      state.metrics = metrics
    },
    ADD_METRIC(state, metric) {
      state.metrics.unshift(metric)
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async logMetrics({ commit }, metricData) {
      console.log('Logging metrics:', metricData)
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const response = await api.post('/health/metrics', metricData)
        console.log('Metrics response:', response.data)
        
        if (response.data.message) {
          // Add the new metric to the state with the returned ID
          const newMetric = {
            id: response.data.metric_id,
            type: metricData.metric_type,
            value: metricData.value,
            systolic: metricData.systolic,
            diastolic: metricData.diastolic,
            unit: metricData.unit,
            notes: metricData.notes,
            timestamp: new Date().toISOString()
          }
          commit('ADD_METRIC', newMetric)
        }
        
        return response.data
      } catch (error) {
        console.error('Error logging metrics:', error)
        const errorMessage = error.response?.data?.error || 'Failed to save metrics'
        commit('SET_ERROR', errorMessage)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async fetchMetrics({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const response = await api.get('/health/metrics')
        commit('SET_METRICS', response.data)
        return response.data
      } catch (error) {
        console.error('Error fetching metrics:', error)
        const errorMessage = error.response?.data?.error || 'Failed to fetch metrics'
        commit('SET_ERROR', errorMessage)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}