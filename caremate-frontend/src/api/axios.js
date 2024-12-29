// src/api/axios.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',  // Make sure this matches your Flask backend URL
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token')
      localStorage.removeItem('userType')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api