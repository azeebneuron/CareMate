// src/views/calls/CallsDashboard.vue
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Main Content Area -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Contact List -->
      <div class="md:col-span-1">
        <div class="bg-white rounded-lg shadow">
          <div class="p-4 border-b">
            <h2 class="text-lg font-medium">Contacts</h2>
          </div>
          <div class="p-4">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search contacts..."
              class="w-full px-3 py-2 border rounded-md mb-4"
            />
            <div class="space-y-2">
              <div
                v-for="contact in filteredContacts"
                :key="contact.id"
                class="p-3 border rounded-lg hover:bg-gray-50 flex justify-between items-center"
              >
                <div>
                  <p class="font-medium">{{ contact.name }}</p>
                  <p class="text-sm text-gray-600">{{ contact.user_type }}</p>
                </div>
                <button
                  @click="initiateCall(contact.id)"
                  class="p-2 text-primary hover:bg-primary hover:text-white rounded-md transition-colors"
                >
                  Call
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Call History -->
      <div class="md:col-span-2">
        <CallHistory />
      </div>
    </div>

    <!-- Active Call Modal -->
    <div 
      v-if="activeCall"
      class="fixed inset-0 bg-black"
    >
      <VideoCall
        :roomId="activeCall.room_id"
        :isInitiator="activeCall.caller_id === currentUserId"
      />
    </div>

    <!-- Incoming Call Modal -->
    <div 
      v-if="incomingCall"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded-lg text-center max-w-sm w-full mx-4">
        <h3 class="text-lg font-medium mb-2">Incoming Call</h3>
        <p class="mb-4">{{ incomingCall.caller.name }} is calling...</p>
        <div class="flex justify-center space-x-4">
          <button
            @click="acceptIncomingCall"
            class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Accept
          </button>
          <button
            @click="rejectIncomingCall"
            class="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Decline
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import CallHistory from '@/components/calls/CallHistory.vue'
import VideoCall from '@/components/calls/VideoCall.vue'

export default {
  name: 'CallsDashboard',
  components: {
    CallHistory,
    VideoCall
  },
  setup() {
    const store = useStore()
    const searchQuery = ref('')

    // Get current user ID from auth store
    const currentUserId = computed(() => store.state.auth.user?.id)

    // Get contacts - in a real app, this would be from a contacts store
    const contacts = ref([])
    const filteredContacts = computed(() => {
      return contacts.value.filter(contact =>
        contact.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const activeCall = computed(() => store.state.calls.activeCall)
    const incomingCall = computed(() => store.state.calls.incomingCall)

    const initiateCall = async (userId) => {
      try {
        await store.dispatch('calls/initiateCall', userId)
      } catch (error) {
        console.error('Error initiating call:', error)
      }
    }

    const acceptIncomingCall = async () => {
      if (incomingCall.value) {
        try {
          await store.dispatch('calls/acceptCall', incomingCall.value.id)
        } catch (error) {
          console.error('Error accepting call:', error)
        }
      }
    }

    const rejectIncomingCall = async () => {
      if (incomingCall.value) {
        try {
          await store.dispatch('calls/rejectCall', incomingCall.value.id)
        } catch (error) {
          console.error('Error rejecting call:', error)
        }
      }
    }

    // Fetch contacts on component mount
    onMounted(async () => {
      try {
        // In a real app, fetch contacts from an API
        const response = await store.dispatch('contacts/fetchContacts')
        contacts.value = response
      } catch (error) {
        console.error('Error fetching contacts:', error)
      }
    })

    return {
      searchQuery,
      filteredContacts,
      currentUserId,
      activeCall,
      incomingCall,
      initiateCall,
      acceptIncomingCall,
      rejectIncomingCall
    }
  }
}
</script>

