// src/views/marketplace/MarketplaceDashboard.vue
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Caregiver Marketplace</h1>
      <p class="text-gray-600">Find qualified and verified caregivers</p>
    </div>

    <CaregiverList v-if="!selectedCaregiverId" />
    <CaregiverProfile 
      v-else 
      :caregiverId="selectedCaregiverId"
      @close="selectedCaregiverId = null"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import CaregiverList from '@/components/marketplace/CaregiverList.vue'
import CaregiverProfile from '@/components/marketplace/CaregiverProfile.vue'

export default {
  name: 'MarketplaceDashboard',
  components: {
    CaregiverList,
    CaregiverProfile
  },
  setup() {
    const store = useStore()
    const route = useRoute()
    const selectedCaregiverId = ref(route.params.id || null)

    onMounted(() => {
      store.dispatch('marketplace/fetchCaregivers')
    })

    return {
      selectedCaregiverId
    }
  }
}
</script>

// src/router/index.js (add these routes)
{
  path: '/marketplace',
  name: 'Marketplace',
  component: MarketplaceDashboard
},
{
  path: '/marketplace/caregiver/:id',
  name: 'CaregiverProfile',
  component: MarketplaceDashboard,
  props: true
}