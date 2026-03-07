<script setup>
import LearnWelcome from '@/components/LearnWelcome.vue';
import LearnSidebar from '@/components/LearnSidebar.vue';
</script>

<template>
    <div class="content max-w-[100vw]">
        <div class="left-0 h-full w-32"> 
            <LearnSidebar />
        </div>
        <div class="h-full">
            <LearnWelcome />
        </div>
        
    </div>
</template>

<style scoped>
.content {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
  background: #f9fafb; /* soft neutral */
}

/* Mobile */
@media (max-width: 768px) {
  .content {
    grid-template-columns: 1fr;
  }
}

</style>