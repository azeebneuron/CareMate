// src/components/marketplace/CaregiverProfileForm.vue
<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-6">{{ isEdit ? 'Edit Profile' : 'Create Profile' }}</h2>
    
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-700">Hourly Rate ($)</label>
        <input
          type="number"
          v-model="form.hourly_rate"
          required
          min="0"
          step="0.01"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Years of Experience</label>
        <input
          type="number"
          v-model="form.experience_years"
          required
          min="0"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Specializations</label>
        <div class="mt-2 space-y-2">
          <div v-for="spec in availableSpecializations" :key="spec.value" class="flex items-center">
            <input
              type="checkbox"
              :value="spec.value"
              v-model="selectedSpecializations"
              class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            />
            <label class="ml-2 text-sm text-gray-700">{{ spec.label }}</label>
          </div>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Bio</label>
        <textarea
          v-model="form.bio"
          rows="4"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        ></textarea>
      </div>

      <div class="flex justify-end space-x-3">
        <button
          type="button"
          @click="$emit('cancel')"
          class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          {{ isEdit ? 'Update Profile' : 'Create Profile' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'CaregiverProfileForm',
  props: {
    isEdit: {
      type: Boolean,
      default: false
    },
    initialData: {
      type: Object,
      default: null
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const store = useStore()
    const form = ref({
      hourly_rate: 0,
      experience_years: 0,
      bio: '',
      specializations: []
    })

    const availableSpecializations = [
      { value: 'elderly_care', label: 'Elderly Care' },
      { value: 'disability_care', label: 'Disability Care' },
      { value: 'medical_care', label: 'Medical Care' },
      { value: 'physiotherapy', label: 'Physiotherapy' },
      { value: 'dementia_care', label: 'Dementia Care' },
      { value: 'palliative_care', label: 'Palliative Care' }
    ]

    const selectedSpecializations = ref([])

    onMounted(() => {
      if (props.initialData) {
        form.value = { ...props.initialData }
        selectedSpecializations.value = props.initialData.specializations.split(',')
      }
    })

    const handleSubmit = async () => {
      try {
        const profileData = {
          ...form.value,
          specializations: selectedSpecializations.value.join(',')
        }
        
        if (props.isEdit) {
          await store.dispatch('marketplace/updateProfile', profileData)
        } else {
          await store.dispatch('marketplace/createProfile', profileData)
        }
        
        emit('submit')
      } catch (error) {
        console.error('Error saving profile:', error)
      }
    }

    return {
      form,
      availableSpecializations,
      selectedSpecializations,
      handleSubmit
    }
  }
}
</script>

