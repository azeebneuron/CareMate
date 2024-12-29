// src/views/Dashboard.vue
<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <div class="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Health Metrics Card -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <!-- You can add an icon here -->
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Health Metrics
                  </dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      View health data
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-5 py-3">
            <router-link
              to="/health"
              class="text-sm font-medium text-primary hover:text-primary-dark"
            >
              View details
            </router-link>
          </div>
        </div>

        <!-- Tasks Card -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <!-- You can add an icon here -->
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Tasks
                  </dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      Manage tasks
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-5 py-3">
            <router-link
              to="/tasks"
              class="text-sm font-medium text-primary hover:text-primary-dark"
            >
              View details
            </router-link>
          </div>
        </div>

        <!-- Emergency Card -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <!-- You can add an icon here -->
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Emergency System
                  </dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      Emergency contacts & alerts
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-5 py-3">
            <router-link
              to="/emergency"
              class="text-sm font-medium text-primary hover:text-primary-dark"
            >
              View details
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>