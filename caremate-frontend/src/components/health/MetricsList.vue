// src/components/health/MetricsList.vue
<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <h3 class="text-lg font-medium mb-4">Recent Health Metrics</h3>
    <div class="space-y-4">
      <div v-for="metric in metrics" :key="metric.id" class="border-b pb-4">
        <div class="flex justify-between items-start">
          <div>
            <h4 class="font-medium capitalize">{{ formatMetricType(metric.metric_type) }}</h4>
            <p class="text-sm text-gray-600">
              {{ formatMetricValue(metric) }}
            </p>
            <p class="text-xs text-gray-500">
              {{ new Date(metric.timestamp).toLocaleString() }}
            </p>
          </div>
        </div>
        <p v-if="metric.additional_notes" class="mt-2 text-sm text-gray-600">
          {{ metric.additional_notes }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'MetricsList',
  setup() {
    const store = useStore()
    const metrics = computed(() => store.state.health.metrics)

    const formatMetricType = (type) => {
      return type.replace('_', ' ')
    }

    const formatMetricValue = (metric) => {
      if (metric.metric_type === 'blood_pressure') {
        return `${metric.systolic}/${metric.diastolic} mmHg`
      }
      
      const units = {
        heart_rate: 'bpm',
        weight: 'kg',
        blood_sugar: 'mg/dL',
        temperature: '°C',
        oxygen: '%'
      }

      return `${metric.value} ${units[metric.metric_type]}`
    }

    return {
      metrics,
      formatMetricType,
      formatMetricValue
    }
  }
}
</script>

