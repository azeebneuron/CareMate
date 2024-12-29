// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Define routes
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/health',
    name: 'Health',
    component: () => import('../views/health/HealthDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('../views/tasks/TaskDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/emergency',
    name: 'Emergency',
    component: () => import('../views/emergency/EmergencyDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/marketplace',
    name: 'Marketplace',
    component: () => import('../views/marketplace/MarketplaceDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/marketplace/profile',
    name: 'CaregiverProfile',
    component: () => import('../views/marketplace/CaregiverProfileManagement.vue'),
    meta: { 
      requiresAuth: true,
      requiresCaregiver: true
    }
  },
  {
    path: '/calls',
    name: 'Calls',
    component: () => import('../views/calls/CallsDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/call/:roomId',
    name: 'VideoCall',
    component: () => import('../components/calls/VideoCall.vue'),
    props: route => ({
      roomId: route.params.roomId,
      isInitiator: route.query.initiator === 'true'
    }),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication and user type
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  const userType = localStorage.getItem('userType')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresCaregiver && userType !== 'caregiver') {
    next('/dashboard')
  } else {
    next()
  }
})

export default router