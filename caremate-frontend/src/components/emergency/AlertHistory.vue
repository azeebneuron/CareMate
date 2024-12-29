// src/components/emergency/AlertHistory.vue
<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-6">Alert History</h2>
    <div class="space-y-4">
      <div
        v-for="alert in alerts"
        :key="alert.id"
        class="p-4 border rounded-lg"
        :class="getAlertClass(alert.status)"
      >
        <div class="flex justify-between items-start">
          <div>
            <span class="font-medium">{{ alert.status }}</span>
            <p class="text-sm text-gray-600">
              Triggered: {{ new Date(alert.created_at).toLocaleString() }}
            </p>
            <p class="text-sm text-gray-600" v-if="alert.resolved_at">
              Resolved: {{ new Date(alert.resolved_at).toLocaleString() }}
            </p>
          </div>
          <button
            v-if="alert.status === 'active'"
            @click="resolveAlert(alert.id)"
            class="px-3 py-1 bg-green-600 text-white rounded-md text-sm"
          >
            Resolve
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'AlertHistory',
  setup() {
    const store = useStore()
    const alerts = ref([])

    const getAlertClass = (status) => {
      const classes = {
        active: 'border-red-500 bg-red-50',
        resolved: 'border-green-500 bg-green-50',
        test: 'border-yellow-500 bg-yellow-50'
      }
      return classes[status] || ''
    }

    const fetchAlerts = async () => {
      try {
        alerts.value = await store.dispatch('emergency/fetchAlerts')
      } catch (error) {
        console.error('Error fetching alerts:', error)
      }
    }

    const resolveAlert = async (alertId) => {
      try {
        await store.dispatch('emergency/resolveAlert', alertId)
        await fetchAlerts()
      } catch (error) {
        console.error('Error resolving alert:', error)
      }
    }

    onMounted(fetchAlerts)

    return {
      alerts,
      getAlertClass,
      resolveAlert
    }
  }
}
</script>