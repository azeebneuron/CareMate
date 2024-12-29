// src/views/health/HealthDashboard.vue
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <MetricsForm />
      <MetricsList />
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useStore } from 'vuex'
import MetricsForm from '@/components/health/MetricsForm.vue'
import MetricsList from '@/components/health/MetricsList.vue'

export default {
  name: 'HealthDashboard',
  components: {
    MetricsForm,
    MetricsList
  },
  setup() {
    const store = useStore()

    onMounted(() => {
      store.dispatch('health/fetchMetrics')
    })
  }
}
</script>