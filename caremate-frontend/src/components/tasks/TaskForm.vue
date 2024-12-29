// src/components/tasks/TaskForm.vue
<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <h3 class="text-lg font-medium mb-4">{{ editMode ? 'Edit Task' : 'Create New Task' }}</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Title</label>
        <input 
          type="text"
          v-model="form.title"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Description</label>
        <textarea 
          v-model="form.description"
          rows="3"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Due Date & Time</label>
        <input 
          type="datetime-local"
          v-model="form.due_time"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Task Type</label>
        <select 
          v-model="form.task_type"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
        >
          <option value="medication">Medication</option>
          <option value="exercise">Exercise</option>
          <option value="appointment">Appointment</option>
          <option value="general">General</option>
        </select>
      </div>

      <div class="flex justify-end space-x-3">
        <button 
          v-if="editMode"
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
          {{ editMode ? 'Update Task' : 'Create Task' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'TaskForm',
  props: {
    editMode: {
      type: Boolean,
      default: false
    },
    taskData: {
      type: Object,
      default: null
    }
  },
  emits: ['cancel', 'taskCreated', 'taskUpdated'],
  setup(props, { emit }) {
    const store = useStore()
    const form = ref({
      title: '',
      description: '',
      due_time: '',
      task_type: 'general'
    })

    onMounted(() => {
      if (props.taskData) {
        form.value = {
          ...props.taskData,
          due_time: new Date(props.taskData.due_time).toISOString().slice(0, 16)
        }
      }
    })

    const handleSubmit = async () => {
      try {
        const payload = {
          ...form.value,
          due_time: new Date(form.value.due_time).toISOString()
        }

        if (props.editMode) {
          await store.dispatch('tasks/updateTask', {
            id: props.taskData.id,
            data: payload
          })
          emit('taskUpdated')
        } else {
          await store.dispatch('tasks/createTask', payload)
          emit('taskCreated')
          // Reset form
          form.value = {
            title: '',
            description: '',
            due_time: '',
            task_type: 'general'
          }
        }
      } catch (error) {
        console.error('Error saving task:', error)
      }
    }

    return {
      form,
      handleSubmit
    }
  }
}
</script>
