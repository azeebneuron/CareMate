// src/components/emergency/EmergencyContacts.vue
<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">Emergency Contacts</h2>
      <button
        @click="showAddForm = true"
        class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
      >
        Add Contact
      </button>
    </div>

    <!-- Contact List -->
    <div class="space-y-4">
      <div
        v-for="contact in contacts"
        :key="contact.id"
        class="flex justify-between items-center p-4 border rounded-lg hover:bg-gray-50"
      >
        <div>
          <h3 class="font-medium">{{ contact.name }}</h3>
          <p class="text-sm text-gray-600">{{ contact.relationship }}</p>
          <p class="text-sm text-gray-600">{{ contact.phone }}</p>
        </div>
        <div class="flex space-x-2">
          <button
            @click="quickCall(contact)"
            class="p-2 text-primary hover:bg-primary hover:text-white rounded-md transition-colors"
          >
            Call
          </button>
          <button
            @click="removeContact(contact.id)"
            class="p-2 text-red-600 hover:bg-red-600 hover:text-white rounded-md transition-colors"
          >
            Remove
          </button>
        </div>
      </div>
    </div>

    <!-- Add Contact Form Modal -->
    <div v-if="showAddForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-medium mb-4">Add Emergency Contact</h3>
        <form @submit.prevent="addContact" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <input
              v-model="newContact.name"
              type="text"
              required
              class="mt-1 block w-full rounded-md border-gray-300"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Phone</label>
            <input
              v-model="newContact.phone"
              type="tel"
              required
              class="mt-1 block w-full rounded-md border-gray-300"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Relationship</label>
            <input
              v-model="newContact.relationship"
              type="text"
              required
              class="mt-1 block w-full rounded-md border-gray-300"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="showAddForm = false"
              class="px-4 py-2 border rounded-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-primary text-white rounded-md"
            >
              Add Contact
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'EmergencyContacts',
  setup() {
    const store = useStore()
    const showAddForm = ref(false)
    const contacts = ref([])
    const newContact = ref({
      name: '',
      phone: '',
      relationship: ''
    })

    const fetchContacts = async () => {
      try {
        contacts.value = await store.dispatch('emergency/fetchContacts')
      } catch (error) {
        console.error('Error fetching contacts:', error)
      }
    }

    const addContact = async () => {
      try {
        await store.dispatch('emergency/addContact', newContact.value)
        showAddForm.value = false
        newContact.value = { name: '', phone: '', relationship: '' }
        await fetchContacts()
      } catch (error) {
        console.error('Error adding contact:', error)
      }
    }

    const removeContact = async (contactId) => {
      if (confirm('Are you sure you want to remove this contact?')) {
        try {
          await store.dispatch('emergency/removeContact', contactId)
          await fetchContacts()
        } catch (error) {
          console.error('Error removing contact:', error)
        }
      }
    }

    const quickCall = (contact) => {
      window.location.href = `tel:${contact.phone}`
    }

    fetchContacts()

    return {
      showAddForm,
      contacts,
      newContact,
      addContact,
      removeContact,
      quickCall
    }
  }
}
</script>

