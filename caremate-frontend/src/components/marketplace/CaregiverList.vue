// src/components/marketplace/CaregiverList.vue
<template>
  <div class="bg-white rounded-lg shadow">
    <!-- Search and Filter Bar -->
    <div class="p-4 border-b">
      <div class="flex flex-col md:flex-row gap-4">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search caregivers..."
          class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        />
        <select
          v-model="specialization"
          class="rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        >
          <option value="">All Specializations</option>
          <option value="elderly_care">Elderly Care</option>
          <option value="disability_care">Disability Care</option>
          <option value="medical_care">Medical Care</option>
          <option value="physiotherapy">Physiotherapy</option>
        </select>
      </div>
    </div>

    <!-- Caregiver Cards -->
    <div class="p-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div 
        v-for="caregiver in filteredCaregivers" 
        :key="caregiver.id"
        class="border rounded-lg p-4 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div>
            <h3 class="font-medium text-lg">{{ caregiver.name }}</h3>
            <div class="flex items-center mt-1">
              <span class="text-yellow-400">★</span>
              <span class="ml-1 text-sm">{{ caregiver.average_rating.toFixed(1) }}</span>
              <span class="ml-1 text-sm text-gray-500">
                ({{ caregiver.reviews.length }} reviews)
              </span>
            </div>
          </div>
          <div class="text-right">
            <p class="font-medium text-primary">${{ caregiver.hourly_rate }}/hr</p>
            <p class="text-sm text-gray-500">{{ caregiver.experience_years }} years exp.</p>
          </div>
        </div>

        <p class="mt-2 text-sm text-gray-600 line-clamp-2">
          {{ formatSpecializations(caregiver.specializations) }}
        </p>

        <div class="mt-4 flex justify-between items-center">
          <button
            @click="viewProfile(caregiver)"
            class="text-primary hover:text-primary-dark font-medium text-sm"
          >
            View Profile
          </button>
          <span 
            v-if="caregiver.verification_status" 
            class="text-green-600 text-sm flex items-center"
          >
            ✓ Verified
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'CaregiverList',
  setup() {
    const router = useRouter()
    const store = useStore()
    const searchQuery = ref('')
    const specialization = ref('')

    const caregivers = computed(() => store.state.marketplace.caregivers)
    
    const filteredCaregivers = computed(() => {
      return caregivers.value.filter(caregiver => {
        const matchesSearch = caregiver.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesSpecialization = !specialization.value || 
          caregiver.specializations.includes(specialization.value)
        return matchesSearch && matchesSpecialization
      })
    })

    const formatSpecializations = (specializations) => {
      return specializations.split(',').map(s => s.trim()).join(', ')
    }

    const viewProfile = (caregiver) => {
      router.push(`/marketplace/caregiver/${caregiver.id}`)
    }

    return {
      searchQuery,
      specialization,
      filteredCaregivers,
      formatSpecializations,
      viewProfile
    }
  }
}
</script>

