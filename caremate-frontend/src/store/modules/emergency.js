// src/store/modules/emergency.js
import api from '@/api/axios'

export default {
  namespaced: true,

  state: () => ({
    contacts: [],
    alerts: [],
    loading: false,
    error: null
  }),

  mutations: {
    SET_CONTACTS(state, contacts) {
      state.contacts = contacts
    },
    ADD_CONTACT(state, contact) {
      state.contacts.push(contact)
    },
    REMOVE_CONTACT(state, contactId) {
      state.contacts = state.contacts.filter(c => c.id !== contactId)
    },
    SET_ALERTS(state, alerts) {
      state.alerts = alerts
    },
    ADD_ALERT(state, alert) {
      state.alerts.unshift(alert)
    },
    UPDATE_ALERT(state, updatedAlert) {
      const index = state.alerts.findIndex(a => a.id === updatedAlert.id)
      if (index !== -1) {
        state.alerts.splice(index, 1, updatedAlert)
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
    async fetchContacts({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/emergency/contacts')
        commit('SET_CONTACTS', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async addContact({ commit }, contactData) {
      try {
        const response = await api.post('/emergency/contacts', contactData)
        commit('ADD_CONTACT', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async removeContact({ commit }, contactId) {
      try {
        await api.delete(`/emergency/contacts/${contactId}`)
        commit('REMOVE_CONTACT', contactId)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async fetchAlerts({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/emergency/alerts')
        commit('SET_ALERTS', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async triggerAlert({ commit }) {
      try {
        const response = await api.post('/emergency/alert')
        commit('ADD_ALERT', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async resolveAlert({ commit }, alertId) {
      try {
        const response = await api.put(`/emergency/alert/${alertId}/resolve`)
        commit('UPDATE_ALERT', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },

    async testAlert({ commit }) {
      try {
        const response = await api.post('/emergency/test')
        commit('ADD_ALERT', { ...response.data, status: 'test' })
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    }
  }
}