
// src/components/tasks/TaskList.vue
<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium">Tasks</h3>
      <div class="flex space-x-2">
        <button 
          @click="showCompleted = !showCompleted"
          class="px-3 py-1 text-sm border rounded-md"
          :class="showCompleted ? 'bg-gray-100' : 'bg-white'"
        >
          {{ showCompleted ? 'Hide Completed' : 'Show Completed' }}
        </button>
      </div>
    </div>

    <div class="space-y-4">
      <div 
        v-for="task in filteredTasks" 
        :key="task.id"
        class="border-b pb-4"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-3">
            <input 
              type="checkbox"
              :checked="task.is_completed"
              @change="toggleTaskStatus(task)"
              class="mt-1"
            />
            <div>
              <h4 
                class="font-medium"
                :class="{'line-through text-gray-500': task.is_completed}"
              >
                {{ task.title }}
              </h4>
              <p class="text-sm text-gray-600">{{ task.description }}</p>
              <div class="flex space-x-4 mt-1 text-sm text-gray-500">
                <span>Due: {{ formatDate(task.due_time) }}</span>
                <span class="capitalize">Type: {{ task.task_type }}</span>
              </div>
            </div>
          </div>
          <div class="flex space-x-2">
            <button 
              @click="editTask(task)"
              class="text-sm text-gray-600 hover:text-primary"
            >
              Edit
            </button>
            <button 
              @click="deleteTask(task.id)"
              class="text-sm text-red-600 hover:text-red-700"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'TaskList',
  emits: ['edit'],
  setup(props, { emit }) {
    const store = useStore()
    const showCompleted = ref(false)

    const tasks = computed(() => store.state.tasks.tasks)
    const filteredTasks = computed(() => {
      return tasks.value.filter(task => showCompleted.value || !task.is_completed)
    })

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    const toggleTaskStatus = async (task) => {
      try {
        await store.dispatch('tasks/updateTask', {
          id: task.id,
          data: { is_completed: !task.is_completed }
        })
      } catch (error) {
        console.error('Error updating task status:', error)
      }
    }

    const deleteTask = async (taskId) => {
      if (confirm('Are you sure you want to delete this task?')) {
        try {
          await store.dispatch('tasks/deleteTask', taskId)
        } catch (error) {
          console.error('Error deleting task:', error)
        }
      }
    }

    const editTask = (task) => {
      emit('edit', task)
    }

    return {
      showCompleted,
      filteredTasks,
      formatDate,
      toggleTaskStatus,
      deleteTask,
      editTask
    }
  }
}
</script>
