// src/views/marketplace/CaregiverProfileManagement.vue
<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white rounded-lg shadow">
      <!-- Profile Header -->
      <div class="p-6 border-b">
        <h1 class="text-2xl font-bold">Caregiver Profile</h1>
        <p class="text-gray-600 mt-1">Manage your professional profile and settings</p>
      </div>

      <!-- Profile Form -->
      <div class="p-6">
        <form @submit.prevent="saveProfile" class="space-y-6">
          <!-- Basic Information -->
          <div>
            <h2 class="text-lg font-medium mb-4">Basic Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Hourly Rate ($)</label>
                <input
                  type="number"
                  v-model="form.hourly_rate"
                  step="0.01"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Years of Experience</label>
                <input
                  type="number"
                  v-model="form.experience_years"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                />
              </div>
            </div>
          </div>

          <!-- Specializations -->
          <div>
            <h2 class="text-lg font-medium mb-4">Specializations</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div v-for="spec in availableSpecializations" :key="spec.value">
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    :value="spec.value"
                    v-model="form.specializations"
                    class="rounded border-gray-300 text-primary focus:ring-primary"
                  />
                  <span class="ml-2 text-sm text-gray-700">{{ spec.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Bio -->
          <div>
            <h2 class="text-lg font-medium mb-4">Professional Bio</h2>
            <textarea
              v-model="form.bio"
              rows="4"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
              placeholder="Tell potential clients about yourself, your experience, and your approach to caregiving..."
            ></textarea>
          </div>

          <!-- Certifications -->
          <div>
            <h2 class="text-lg font-medium mb-4">Certifications & Training</h2>
            <div class="space-y-2">
              <div v-for="(cert, index) in form.certifications" :key="index" class="flex gap-2">
                <input
                  type="text"
                  v-model="cert.name"
                  placeholder="Certification name"
                  class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                />
                <input
                  type="date"
                  v-model="cert.date"
                  class="rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                />
                <button 
                  type="button"
                  @click="removeCertification(index)"
                  class="px-2 py-1 text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </div>
              <button 
                type="button"
                @click="addCertification"
                class="text-primary hover:text-primary-dark text-sm font-medium"
              >
                + Add Certification
              </button>
            </div>
          </div>

          <!-- Availability -->
          <div>
            <h2 class="text-lg font-medium mb-4">Availability</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div v-for="day in weekDays" :key="day.value">
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    :value="day.value"
                    v-model="form.availability"
                    class="rounded border-gray-300 text-primary focus:ring-primary"
                  />
                  <span class="ml-2 text-sm text-gray-700">{{ day.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end">
            <button
              type="submit"
              class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              :disabled="saving"
            >
              {{ saving ? 'Saving...' : 'Save Profile' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Profile Stats -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-2">Total Reviews</h3>
        <p class="text-3xl font-bold">{{ profileStats.totalReviews }}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-2">Average Rating</h3>
        <p class="text-3xl font-bold">{{ profileStats.averageRating.toFixed(1) }}/5.0</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-2">Profile Views</h3>
        <p class="text-3xl font-bold">{{ profileStats.profileViews }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'CaregiverProfileManagement',
  setup() {
    const store = useStore()
    const router = useRouter()
    const saving = ref(false)

    const form = ref({
      hourly_rate: 0,
      experience_years: 0,
      specializations: [],
      bio: '',
      certifications: [],
      availability: []
    })

    const availableSpecializations = [
      { value: 'elderly_care', label: 'Elderly Care' },
      { value: 'disability_care', label: 'Disability Care' },
      { value: 'medical_care', label: 'Medical Care' },
      { value: 'physiotherapy', label: 'Physiotherapy' },
      { value: 'dementia_care', label: 'Dementia Care' },
      { value: 'palliative_care', label: 'Palliative Care' }
    ]

    const weekDays = [
      { value: 'monday', label: 'Monday' },
      { value: 'tuesday', label: 'Tuesday' },
      { value: 'wednesday', label: 'Wednesday' },
      { value: 'thursday', label: 'Thursday' },
      { value: 'friday', label: 'Friday' },
      { value: 'saturday', label: 'Saturday' },
      { value: 'sunday', label: 'Sunday' }
    ]

    const profileStats = ref({
      totalReviews: 0,
      averageRating: 0,
      profileViews: 0
    })

    const addCertification = () => {
      form.value.certifications.push({ name: '', date: '' })
    }

    const removeCertification = (index) => {
      form.value.certifications.splice(index, 1)
    }

    const saveProfile = async () => {
      saving.value = true
      try {
        const profileData = {
          ...form.value,
          specializations: form.value.specializations.join(',')
        }
        await store.dispatch('marketplace/updateCaregiverProfile', profileData)
        // Show success message
      } catch (error) {
        console.error('Error saving profile:', error)
        // Show error message
      } finally {
        saving.value = false
      }
    }

    const loadProfile = async () => {
      try {
        const profile = await store.dispatch('marketplace/fetchCaregiverProfile')
        if (profile) {
          form.value = {
            ...profile,
            specializations: profile.specializations.split(','),
            certifications: profile.certifications || [],
            availability: profile.availability || []
          }
        }
        // Load profile stats
        profileStats.value = await store.dispatch('marketplace/fetchProfileStats')
      } catch (error) {
        console.error('Error loading profile:', error)
      }
    }

    onMounted(loadProfile)

    return {
      form,
      saving,
      availableSpecializations,
      weekDays,
      profileStats,
      addCertification,
      removeCertification,
      saveProfile
    }
  }
}
</script>