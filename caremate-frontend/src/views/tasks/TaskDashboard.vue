// src/views/tasks/TaskDashboard.vue
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="space-y-6">
      <TaskForm 
        v-if="!editingTask"
        @taskCreated="handleTaskCreated" 
      />
      <TaskForm 
        v-else
        :editMode="true"
        :taskData="editingTask"
        @cancel="cancelEdit"
        @taskUpdated="handleTaskUpdated"
      />
      <TaskList @edit="startEdit" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import TaskForm from '@/components/tasks/TaskForm.vue'
import TaskList from '@/components/tasks/TaskList.vue'

export default {
  name: 'TaskDashboard',
  components: {
    TaskForm,
    TaskList
  },
  setup() {
    const store = useStore()
    const editingTask = ref(null)

    onMounted(() => {
      store.dispatch('tasks/fetchTasks')
    })

    const startEdit = (task) => {
      editingTask.value = task
    }

    const cancelEdit = () => {
      editingTask.value = null
    }

    const handleTaskCreated = () => {
      // You could add a success notification here
    }

    const handleTaskUpdated = () => {
      editingTask.value = null
      // You could add a success notification here
    }

    return {
      editingTask,
      startEdit,
      cancelEdit,
      handleTaskCreated,
      handleTaskUpdated
    }
  }
}
</script>