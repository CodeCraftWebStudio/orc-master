<script setup>
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
  message: String,
})

const emit = defineEmits(['close'])
function closeError() {
    localStorage.setItem('isErrorPresent', false);
    $emit('close');
}
</script>

<template>
    <div class="notification" v-if="message">
      <span class="message">{{ message }}</span>
        <button class="close" @click="closeError">✕</button>
    </div>
</template>

<style scoped>
.notification {
  position: fixed;
  top: 25%;
  left: 50%;
  align-self: center;

  transform: translateX(-50%);
  width: 50%;
  height: 50%;
  z-index: 100000000000000000;

  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);

  border-radius: 0 0 14px 14px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);

  padding: 1rem 1.25rem;

  display: flex;
  justify-content: space-between;
  align-items: center;

  animation-name: slideDown;
  animation-duration: 2s;

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
.close:hover {
    cursor: pointer;
    padding: 2rem;
    background: rgba(0, 0, 255, 0.01);
}

@keyframes slideDown {
    from {
        top: -50%;
    }
    to {
        top: 25%;
    }
}
</style>
