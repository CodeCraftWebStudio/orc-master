<script setup>
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
  message: String,
  actions: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close'])

function handleAction(action) {
  if (action.onClick) {
    action.onClick()
  }
  emit('close')
}
</script>

<template>
  <transition name="slide-down">
    <div class="notification" v-if="message">
      <span class="message">{{ message }}</span>

      <div class="actions">
        <button
          v-for="(action, i) in actions"
          :key="i"
          @click="handleAction(action)"
        >
          {{ action.label }}
        </button>

        <button class="close" @click="$emit('close')">✕</button>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.notification {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: min(900px, 95%);
  z-index: 1000;

  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);

  border-radius: 0 0 14px 14px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);

  padding: 1rem 1.25rem;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message {
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

button {
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.close {
  background: transparent;
  font-size: 1.1rem;
}
</style>
