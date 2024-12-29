// src/components/emergency/EmergencyButton.vue
<template>
  <div class="text-center">
    <button
      @click="activateEmergency"
      :disabled="isActivating"
      class="w-48 h-48 rounded-full bg-red-600 hover:bg-red-700 text-white font-bold text-xl shadow-lg transform hover:scale-105 transition-all flex items-center justify-center"
      :class="{'opacity-75': isActivating}"
    >
      <span v-if="!isActivating">EMERGENCY</span>
      <span v-else>Alerting...</span>
    </button>

    <!-- Confirmation Modal -->
    <div v-if="showConfirmation" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg p-6 max-w-sm w-full">
        <h3 class="text-lg font-medium mb-4">Confirm Emergency Alert</h3>
        <p class="mb-4">This will notify all your emergency contacts. Continue?</p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showConfirmation = false"
            class="px-4 py-2 border rounded-md"
          >
            Cancel
          </button>
          <button
            @click="confirmEmergency"
            class="px-4 py-2 bg-red-600 text-white rounded-md"
          >
            Confirm Emergency
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'EmergencyButton',
  setup() {
    const store = useStore()
    const isActivating = ref(false)
    const showConfirmation = ref(false)

    const activateEmergency = () => {
      showConfirmation.value = true
    }

    const confirmEmergency = async () => {
      try {
        isActivating.value = true
        showConfirmation.value = false
        await store.dispatch('emergency/triggerAlert')
        // Success notification could be added here
      } catch (error) {
        console.error('Error triggering emergency:', error)
      } finally {
        isActivating.value = false
      }
    }

    return {
      isActivating,
      showConfirmation,
      activateEmergency,
      confirmEmergency
    }
  }
}
</script>

