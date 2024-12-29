// src/components/calls/CallHistory.vue
<template>
  <div class="bg-white rounded-lg shadow">
    <div class="p-4 border-b">
      <h2 class="text-lg font-medium">Call History</h2>
    </div>
    <div class="p-4">
      <div v-for="call in calls" :key="call.id" class="mb-4 last:mb-0">
        <div class="flex justify-between items-start p-4 border rounded-lg hover:bg-gray-50">
          <div>
            <p class="font-medium">
              {{ call.caller.id === currentUserId ? call.callee.name : call.caller.name }}
            </p>
            <p class="text-sm text-gray-600">
              {{ formatDate(call.start_time) }}
            </p>
            <p class="text-sm text-gray-500">
              Duration: {{ calculateDuration(call.start_time, call.end_time) }}
            </p>
          </div>
          <div class="flex items-center">
            <span 
              class="px-2 py-1 text-sm rounded"
              :class="getStatusClass(call.status)"
            >
              {{ call.status }}
            </span>
            <button
              v-if="call.status === 'ended'"
              @click="initiateCall(call.caller.id === currentUserId ? call.callee.id : call.caller.id)"
              class="ml-4 text-primary hover:text-primary-dark"
            >
              Call Again
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'CallHistory',
  setup() {
    const store = useStore()
    const calls = ref([])
    const currentUserId = store.state.auth.user?.id

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    const calculateDuration = (start, end) => {
      if (!end) return 'In progress'
      const duration = new Date(end) - new Date(start)
      const minutes = Math.floor(duration / 60000)
      const seconds = Math.floor((duration % 60000) / 1000)
      return `${minutes}m ${seconds}s`
    }

    const getStatusClass = (status) => {
      const classes = {
        'active': 'bg-green-100 text-green-800',
        'ended': 'bg-gray-100 text-gray-800',
        'missed': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }

    const initiateCall = async (userId) => {
      try {
        await store.dispatch('calls/initiateCall', userId)
      } catch (error) {
        console.error('Error initiating call:', error)
      }
    }

    const fetchCalls = async () => {
      try {
        const response = await store.dispatch('calls/fetchHistory')
        calls.value = response
      } catch (error) {
        console.error('Error fetching call history:', error)
      }
    }

    onMounted(fetchCalls)

    return {
      calls,
      currentUserId,
      formatDate,
      calculateDuration,
      getStatusClass,
      initiateCall
    }
  }
}
</script>