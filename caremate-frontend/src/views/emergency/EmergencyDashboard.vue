// src/views/emergency/EmergencyDashboard.vue
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Emergency Header -->
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-900">Emergency System</h1>
      <p class="mt-2 text-gray-600">Quick access to emergency assistance and contacts</p>
    </div>

    <!-- Main Grid Layout -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Left Column -->
      <div class="space-y-8">
        <!-- Emergency Button Section -->
        <div class="bg-white rounded-lg shadow p-8 text-center">
          <EmergencyButton />
          <div class="mt-4">
            <button 
              @click="testEmergencySystem" 
              class="text-sm text-gray-600 hover:text-primary"
            >
              Test Emergency System
            </button>
          </div>
        </div>

        <!-- Quick Dial Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-bold mb-4">Quick Dial</h2>
          <div class="grid grid-cols-2 gap-4">
            <a 
              href="tel:911" 
              class="flex items-center justify-center p-4 bg-red-100 text-red-700 rounded-lg hover:bg-red-200"
            >
              Emergency (911)
            </a>
            <button 
              v-for="contact in quickDialContacts" 
              :key="contact.id"
              @click="quickDial(contact.phone)"
              class="flex items-center justify-center p-4 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              {{ contact.name }}
            </button>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="space-y-8">
        <!-- Emergency Contacts Section -->
        <EmergencyContacts />
        
        <!-- Alert History Section -->
        <AlertHistory />
      </div>
    </div>

    <!-- Location Sharing Status -->
    <div class="mt-8 bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="font-medium">Location Sharing</h3>
          <p class="text-sm text-gray-600">
            {{ locationEnabled ? 'Location sharing is enabled' : 'Location sharing is disabled' }}
          </p>
        </div>
        <button 
          @click="toggleLocation"
          class="px-4 py-2 rounded-md"
          :class="locationEnabled ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
        >
          {{ locationEnabled ? 'Enabled' : 'Enable Location' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import EmergencyButton from '@/components/emergency/EmergencyButton.vue'
import EmergencyContacts from '@/components/emergency/EmergencyContacts.vue'
import AlertHistory from '@/components/emergency/AlertHistory.vue'

export default {
  name: 'EmergencyDashboard',
  components: {
    EmergencyButton,
    EmergencyContacts,
    AlertHistory
  },
  setup() {
    const store = useStore()
    const locationEnabled = ref(false)

    // Get the first 3 emergency contacts for quick dial
    const quickDialContacts = computed(() => {
      return store.state.emergency.contacts.slice(0, 3)
    })

    const toggleLocation = async () => {
      try {
        if (!locationEnabled.value) {
          // Request location permission
          const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject)
          })

          // Store location in emergency system
          await store.dispatch('emergency/updateLocation', {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          })

          locationEnabled.value = true
        } else {
          // Disable location sharing
          await store.dispatch('emergency/updateLocation', null)
          locationEnabled.value = false
        }
      } catch (error) {
        console.error('Error toggling location:', error)
        // Show error notification to user
      }
    }

    const quickDial = (phoneNumber) => {
      window.location.href = `tel:${phoneNumber}`
    }

    const testEmergencySystem = async () => {
      try {
        await store.dispatch('emergency/testAlert')
        // Show success notification
      } catch (error) {
        console.error('Error testing emergency system:', error)
        // Show error notification
      }
    }

    onMounted(() => {
      // Check if location is already enabled
      navigator.geolocation.getCurrentPosition(
        () => { locationEnabled.value = true },
        () => { locationEnabled.value = false }
      )
    })

    return {
      locationEnabled,
      quickDialContacts,
      toggleLocation,
      quickDial,
      testEmergencySystem
    }
  }
}
</script>

