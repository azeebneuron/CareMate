
// src/store/modules/tasks.js
import api from '@/api/axios'

export default {
  namespaced: true,
  
  state: () => ({
    tasks: [],
    loading: false,
    error: null
  }),
  
  mutations: {
    SET_TASKS(state, tasks) {
      state.tasks = tasks
    },
    ADD_TASK(state, task) {
      state.tasks.unshift(task)
    },
    UPDATE_TASK(state, updatedTask) {
      const index = state.tasks.findIndex(t => t.id === updatedTask.id)
      if (index !== -1) {
        state.tasks.splice(index, 1, updatedTask)
      }
    },
    DELETE_TASK(state, taskId) {
      state.tasks = state.tasks.filter(t => t.id !== taskId)
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async fetchTasks({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/tasks')
        commit('SET_TASKS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async createTask({ commit }, taskData) {
      try {
        const response = await api.post('/tasks', taskData)
        commit('ADD_TASK', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },
    
    async updateTask({ commit }, { id, data }) {
      try {
        const response = await api.put(`/tasks/${id}`, data)
        commit('UPDATE_TASK', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    },
    
    async deleteTask({ commit }, taskId) {
      try {
        await api.delete(`/tasks/${taskId}`)
        commit('DELETE_TASK', taskId)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      }
    }
  }
}