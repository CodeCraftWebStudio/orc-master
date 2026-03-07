<script setup>
import { useRouter } from 'vue-router'

const router = useRouter();

function logout() {
    localStorage.clear();
    router.push('/');
}
</script>


<template>
    <h2> Are you sure you want to logout? There's no going back. </h2>
    <button @click="logout">Logout Anyway</button>
</template>


<style scoped>

</style>