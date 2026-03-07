<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const avatarUrl = ref('')

onMounted(() => {
  const saved = localStorage.getItem('avatar_url')
  if (saved) avatarUrl.value = saved
})

function setAvatarUrl(e) {
  const file = e.target.files?.[0]

  // If file exists (file upload)
  if (file) {
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file.')
      return
    }

    const reader = new FileReader()
    reader.onload = () => {
      avatarUrl.value = reader.result
      localStorage.setItem('avatar_url', avatarUrl.value)
    }
    reader.readAsDataURL(file)
  } 
  // If text input
  else {
    avatarUrl.value = e.target.value
    localStorage.setItem('avatar_url', avatarUrl.value)
  }
}
</script>

<template>
  <div
    class="absolute left-full top-1/2 transform -translate-y-1/2 ml-3 p-3 w-56 bg-gray-100 text-gray-800 rounded-lg shadow-lg opacity-0 pointer-events-none transition-opacity duration-300 hover:opacity-100 group-hover:opacity-100"
  >
    <!-- Avatar Preview -->
    <div class="flex justify-center mb-3">
      <img
        v-if="avatarUrl"
        :src="avatarUrl"
        class="w-20 h-20 rounded-full object-cover border"
      />
      <div
        v-else
        class="w-20 h-20 rounded-full bg-gray-300 flex items-center justify-center text-sm text-gray-600"
      >
        No Avatar
      </div>
    </div>

    <!-- Upload File -->
    <label class="block mb-1 text-sm font-medium">Upload Avatar</label>
    <input
      type="file"
      accept="image/*"
      @change="setAvatarUrl"
      class="w-full text-sm text-gray-700 border border-gray-300 rounded px-2 py-1 mb-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
    />

    <!-- Image URL -->
    <label class="block mb-1 text-sm font-medium">Image URL</label>
    <input
      type="text"
      placeholder="Paste image URL"
      @change="setAvatarUrl"
      class="w-full text-sm text-gray-700 border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-400"
    />

    <!-- Remove Button -->
    <button
      v-if="avatarUrl"
      @click="() => { avatarUrl = ''; localStorage.removeItem('avatar_url') }"
      class="mt-3 w-full bg-red-500 text-white text-sm py-1 rounded hover:bg-red-600 transition"
    >
      Remove Avatar
    </button>
  </div>
</template>