// src/components/marketplace/ContactCaregiverModal.vue
<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg max-w-md w-full p-6">
      <h3 class="text-lg font-medium mb-4">Contact {{ caregiver.name }}</h3>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Message</label>
          <textarea
            v-model="message"
            rows="4"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Preferred Contact Time</label>
          <input
            type="datetime-local"
            v-model="preferredTime"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
          />
        </div>

        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Send Message
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'ContactCaregiverModal',
  props: {
    caregiver: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'sent'],
  setup(props, { emit }) {
    const store = useStore()
    const message = ref('')
    const preferredTime = ref('')

    const handleSubmit = async () => {
      try {
        await store.dispatch('marketplace/contactCaregiver', {
          caregiverId: props.caregiver.id,
          message: message.value,
          preferredTime: preferredTime.value
        })
        emit('sent')
        emit('close')
      } catch (error) {
        console.error('Error sending message:', error)
      }
    }

    return {
      message,
      preferredTime,
      handleSubmit
    }
  }
}
</script>