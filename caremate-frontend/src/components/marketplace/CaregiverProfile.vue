// src/components/marketplace/CaregiverProfile.vue
<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex justify-between items-start">
      <div>
        <h2 class="text-2xl font-bold">{{ caregiver.name }}</h2>
        <div class="flex items-center mt-2">
          <span class="text-yellow-400">★</span>
          <span class="ml-1">{{ caregiver.average_rating.toFixed(1) }}</span>
          <span class="ml-1 text-gray-500">({{ caregiver.reviews.length }} reviews)</span>
        </div>
      </div>
      <div class="text-right">
        <p class="text-2xl font-bold text-primary">${{ caregiver.hourly_rate }}/hr</p>
        <p class="text-gray-600">{{ caregiver.experience_years }} years experience</p>
      </div>
    </div>

    <div class="mt-6">
      <h3 class="font-medium mb-2">Specializations</h3>
      <div class="flex flex-wrap gap-2">
        <span 
          v-for="spec in specializations" 
          :key="spec"
          class="px-3 py-1 bg-gray-100 rounded-full text-sm"
        >
          {{ spec }}
        </span>
      </div>
    </div>

    <!-- Reviews Section -->
    <div class="mt-8">
      <div class="flex justify-between items-center mb-4">
        <h3 class="font-medium">Reviews</h3>
        <button 
          @click="showReviewForm = true"
          class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
        >
          Write Review
        </button>
      </div>

      <div v-if="showReviewForm" class="mb-6 p-4 border rounded-lg">
        <h4 class="font-medium mb-3">Write a Review</h4>
        <form @submit.prevent="submitReview">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Rating</label>
            <select 
              v-model="newReview.rating"
              required
              class="mt-1 block w-full rounded-md border-gray-300"
            >
              <option v-for="n in 5" :key="n" :value="n">{{ n }} stars</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Comment</label>
            <textarea
              v-model="newReview.comment"
              rows="3"
              required
              class="mt-1 block w-full rounded-md border-gray-300"
            ></textarea>
          </div>
          <div class="flex justify-end gap-3">
            <button 
              type="button"
              @click="showReviewForm = false"
              class="px-4 py-2 border rounded-md"
            >
              Cancel
            </button>
            <button 
              type="submit"
              class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
            >
              Submit Review
            </button>
          </div>
        </form>
      </div>

      <div class="space-y-4">
        <div 
          v-for="review in caregiver.reviews" 
          :key="review.id"
          class="border-b pb-4"
        >
          <div class="flex justify-between items-start">
            <div>
              <div class="flex items-center">
                <span class="text-yellow-400">
                  {{ '★'.repeat(review.rating) }}
                  <span class="text-gray-300">{{ '★'.repeat(5 - review.rating) }}</span>
                </span>
              </div>
              <p class="mt-1">{{ review.comment }}</p>
            </div>
            <span class="text-sm text-gray-500">
              {{ new Date(review.created_at).toLocaleDateString() }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'

export default {
  name: 'CaregiverProfile',
  props: {
    caregiverId: {
      type: [String, Number],
      required: true
    }
  },
  setup(props) {
    const store = useStore()
    const route = useRoute()
    const showReviewForm = ref(false)
    const newReview = ref({
      rating: 5,
      comment: ''
    })

    const caregiver = computed(() => 
      store.state.marketplace.caregivers.find(c => c.id === parseInt(props.caregiverId))
    )

    const specializations = computed(() => 
      caregiver.value?.specializations.split(',').map(s => s.trim()) || []
    )

    const submitReview = async () => {
      try {
        await store.dispatch('marketplace/addReview', {
          caregiverId: props.caregiverId,
          ...newReview.value
        })
        showReviewForm.value = false
        newReview.value = { rating: 5, comment: '' }
      } catch (error) {
        console.error('Error submitting review:', error)
      }
    }

    return {
      caregiver,
      specializations,
      showReviewForm,
      newReview,
      submitReview
    }
  }
}
</script>

