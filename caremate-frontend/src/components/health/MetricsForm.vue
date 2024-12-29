// src/components/health/MetricsForm.vue
<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <h3 class="text-lg font-medium mb-4">Log Health Metrics</h3>
    <!-- Error display -->
    <div v-if="error" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ error }}
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Metric Type</label>
        <select 
          v-model="form.metric_type"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        >
          <option value="blood_pressure">Blood Pressure</option>
          <option value="heart_rate">Heart Rate</option>
          <option value="weight">Weight</option>
          <option value="blood_sugar">Blood Sugar</option>
          <option value="temperature">Temperature</option>
          <option value="oxygen_level">Oxygen Level</option>
        </select>
      </div>

      <template v-if="form.metric_type === 'blood_pressure'">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Systolic (mmHg)</label>
            <input 
              type="number" 
              v-model="form.systolic"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Diastolic (mmHg)</label>
            <input 
              type="number" 
              v-model="form.diastolic"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
            />
          </div>
        </div>
      </template>
      
      <template v-else>
        <div>
          <label class="block text-sm font-medium text-gray-700">Value ({{ getUnit(form.metric_type) }})</label>
          <input 
            type="number" 
            v-model="form.value"
            step="0.1"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
          />
        </div>
      </template>

      <div>
        <label class="block text-sm font-medium text-gray-700">Notes</label>
        <textarea 
          v-model="form.notes"
          rows="2"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        ></textarea>
      </div>

      <button 
        type="submit"
        :disabled="loading"
        class="w-full bg-primary text-white py-2 px-4 rounded-md hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
      >
        {{ loading ? 'Saving...' : 'Save Metrics' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'MetricsForm',
  setup() {
    const store = useStore()
    const loading = computed(() => store.state.health.loading)
    const error = computed(() => store.state.health.error)

    const form = ref({
      metric_type: 'blood_pressure',
      value: '',
      systolic: '',
      diastolic: '',
      notes: ''
    })

    const getUnit = (metricType) => {
      const units = {
        blood_pressure: 'mmHg',
        heart_rate: 'bpm',
        weight: 'kg',
        blood_sugar: 'mg/dL',
        temperature: '°C',
        oxygen_level: '%'
      }
      return units[metricType] || ''
    }

    const handleSubmit = async () => {
      try {
        const payload = {
          metric_type: form.value.metric_type,
          unit: getUnit(form.value.metric_type),
          notes: form.value.notes
        }

        if (form.value.metric_type === 'blood_pressure') {
          if (!form.value.systolic || !form.value.diastolic) {
            throw new Error('Both systolic and diastolic values are required for blood pressure')
          }
          payload.systolic = parseFloat(form.value.systolic)
          payload.diastolic = parseFloat(form.value.diastolic)
        } else {
          if (!form.value.value) {
            throw new Error('Value is required')
          }
          payload.value = parseFloat(form.value.value)
        }

        console.log('Submitting metrics:', payload)
        await store.dispatch('health/logMetrics', payload)
        
        // Reset form after successful submission
        form.value = {
          metric_type: 'blood_pressure',
          value: '',
          systolic: '',
          diastolic: '',
          notes: ''
        }
      } catch (error) {
        console.error('Error submitting metrics:', error)
      }
    }

    return {
      form,
      loading,
      error,
      handleSubmit,
      getUnit
    }
  }
}
</script>