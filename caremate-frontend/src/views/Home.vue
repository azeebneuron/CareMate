// src/views/Home.vue
<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Welcome to CareMate
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          Connecting caregivers with those who need care
        </p>
        <div class="space-x-4">
          <router-link
            to="/login"
            class="inline-block bg-primary text-white px-6 py-2 rounded-md hover:bg-primary-dark"
          >
            Sign In
          </router-link>
          <router-link
            to="/register"
            class="inline-block bg-white text-primary px-6 py-2 rounded-md border border-primary hover:bg-gray-50"
          >
            Register
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>