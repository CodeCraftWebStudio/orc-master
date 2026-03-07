<script setup>
import TheWelcome from '../components/TheWelcome.vue'
import { ref } from 'vue';
import { useUserStore } from '@/stores/counter';

// const userStore = useUserStore();

</script>

<template>
  <main>
    <div><TheWelcome /></div>
    <!-- <div v-else> Welcome, it appears that you've registered. </div> -->
  </main>
</template>
