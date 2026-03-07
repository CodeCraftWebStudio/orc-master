<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useApiStore } from '@/stores/counter'
const router = useRouter()
const api = useApiStore();
const name = ref('')

const level = ref('')
const section = ref('')
const isSubmitting = ref(false)
const error = ref('')

const levels = ['JSS1', 'JSS2', 'JSS3', 'SS1', 'SS2', 'SS3', 'Outgone']
const sections = ['A', 'B', 'C', 'D', 'E']

const isOutgone = computed(() => level.value === 'Outgone')

watch(isOutgone, (val) => {
  if (val) section.value = ''
})

const finalClass = computed(() => {
  if (isOutgone.value) return 'Outgone'
  if (!level.value || !section.value) return ''
  return `${level.value}${section.value}`
})

const isValid = computed(() => {
  if (name.value.trim().length < 2) return false
  if (!level.value) return false
  if (!isOutgone.value && !section.value) return false
  return true
})

async function submitRegistration() {
  if (!isValid.value) {
    error.value = 'Please complete all required fields.'
    return
  }

  isSubmitting.value = true
  error.value = ''

  try {
    /**
     * 🔌 BACKEND CALL GOES HERE
     * payload:
     * {
     *   name: name.value,
     *   class: finalClass.value
     *   session_key: localStorage.getItem('key')
     * }
     */
     const res = await api.apiFetch('/user/registerUser', 'POST', {name: name.value, school_class: finalClass.value, session_key: localStorage.getItem('key')});
     if (res.session_key) {
      api.setSessionKey(res.session_key);
     }
    console.log(`Registration key: ${localStorage.getItem('key')}`)
    router.push('/')
  } catch (e) {
    error.value = 'Something went wrong. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>


<template>
  <div class="min-h-screen flex items-center justify-center bg-white px-4 w-full">
    <div class="w-full max-w-md bg-white shadow-lg rounded-2xl p-6 border h-full content">

      <h1 class=" flex text-2xl font-bold text-red-600 mb-2 items-center justify-center">
        Join ORC Web
      </h1>

      <p class="flex text-sm text-gray-600 mb-6 items-center justify-center">
        Tell us a bit about yourself. No passwords, no emails.
      </p>
      <div class="space"></div>
      <div class="space"></div>
      <form @submit.prevent="submitRegistration" class="space-y-4">

        <!-- Name -->
        <div>
          <label class="block text-sm font-medium mb-1">
            Full Name
          </label>
          <input
            v-model="name"
            type="text"
            placeholder="e.g. Alex Johnson"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none"
          />
        </div>
        <div class="space"></div>
        <!-- Class -->

<!-- Level -->
<div>
  <label class="block text-sm font-medium mb-1">
    Level
  </label>
  <select
    v-model="level"
    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none"
  >
    <option value="" disabled>Select level</option>
    <option v-for="l in levels" :key="l" :value="l">
      {{ l }}
    </option>
  </select>
</div>
<div class="space"></div>
<!-- Class Section -->
    <div>
    <label class="block text-sm font-medium mb-1">
        Class
    </label>
    <select
        v-model="section"
        :disabled="isOutgone"
        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none
            disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
    >
        <option value="" disabled>
        {{ isOutgone ? 'Not applicable' : 'Select class' }}
        </option>
        <option v-for="s in sections" :key="s" :value="s">
        {{ s }}
        </option>
    </select>
    </div> 
<div class="space"></div>

        <!-- Error -->
        <p v-if="error" class="text-sm text-red-600">
          {{ error }}
        </p>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="!isValid || isSubmitting"
          class="w-full py-2 rounded-lg font-semibold transition
                 bg-red-600 text-white
                 disabled:opacity-50 disabled:cursor-not-allowed
                 hover:bg-red-700"
        >
          {{ isSubmitting ? 'Joining...' : 'Join' }}
        </button>
        <div class="space"></div>
        <button class="w-full py-2 rounded-lg font-semibold transition bg-red-600 text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-red-700">
          <RouterLink to="/executive">Sign Up as an Executive</RouterLink>
        </button>

      </form>

      <p class="text-xs text-gray-500 mt-6 text-center">
        You can update your role later. The President assigns positions.
      </p>
    </div>
  </div>
</template>


<style scoped>
    .content {
        padding: 20px;
    }
    .space {
      padding: 5px;
    }
</style>