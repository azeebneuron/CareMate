// src/store/modules/calls.js
import api from '@/api/axios'
import router from '@/router'

export default {
  namespaced: true,

  state: () => ({
    callHistory: [],
    activeCall: null,
    loading: false,
    error: null,
    incomingCall: null
  }),

  mutations: {
    SET_CALL_HISTORY(state, history) {
      state.callHistory = history
    },
    SET_ACTIVE_CALL(state, call) {
      state.activeCall = call
    },
    SET_INCOMING_CALL(state, call) {
      state.incomingCall = call
    },
    UPDATE_CALL_STATUS(state, { callId, status }) {
      const call = state.callHistory.find(c => c.id === callId)
      if (call) {
        call.status = status
      }
    },
    ADD_TO_HISTORY(state, call) {
      state.callHistory.unshift(call)
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },

  actions: {
    async fetchHistory({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/calls/history')
        commit('SET_CALL_HISTORY', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async initiateCall({ commit }, userId) {
      try {
        const response = await api.post('/calls/start', {
          callee_id: userId
        })
        
        commit('SET_ACTIVE_CALL', response.data)
        commit('ADD_TO_HISTORY', response.data)
        
        router.push({
          name: 'VideoCall',
          params: { 
            roomId: response.data.room_id,
            isInitiator: true
          }
        })
        
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async endCall({ commit }, roomId) {
      try {
        const response = await api.post(`/calls/${roomId}/end`)
        commit('UPDATE_CALL_STATUS', {
          callId: response.data.id,
          status: 'ended'
        })
        commit('SET_ACTIVE_CALL', null)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async acceptCall({ commit }, callId) {
      try {
        const response = await api.post(`/calls/${callId}/accept`)
        commit('UPDATE_CALL_STATUS', {
          callId,
          status: 'active'
        })
        commit('SET_ACTIVE_CALL', response.data)
        commit('SET_INCOMING_CALL', null)
        
        router.push({
          name: 'VideoCall',
          params: { 
            roomId: response.data.room_id,
            isInitiator: false
          }
        })
        
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async rejectCall({ commit }, callId) {
      try {
        const response = await api.post(`/calls/${callId}/reject`)
        commit('UPDATE_CALL_STATUS', {
          callId,
          status: 'missed'
        })
        commit('SET_INCOMING_CALL', null)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    handleIncomingCall({ commit }, callData) {
      commit('SET_INCOMING_CALL', callData)
    }
  },

  getters: {
    hasActiveCall: state => !!state.activeCall,
    hasIncomingCall: state => !!state.incomingCall
  }
}