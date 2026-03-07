<script setup>
// This component receives ONE section 
defineProps({
  section: Object
})
</script>

<template>
  <section>
    <!-- Section title -->
    <h2>{{ section.title }}</h2>

    <!-- Render rich text safely -->
    <PortableText :value="section.blocks" />

    <!-- Render subsections (if any) -->
    <div v-if="section.children?.length">
      <SectionRenderer
        v-for="child in section.children"
        :key="child._key"
        :section="child"
      />
    </div>
  </section>
</template>
