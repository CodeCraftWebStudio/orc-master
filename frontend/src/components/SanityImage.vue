<!-- components/SanityImage.vue -->
<template>
  <img
    :src="imageUrl"
    :alt="value.alt || ''"
    :style="{ display: isInline ? 'inline-block' : 'block' }"
    loading="lazy"
  />
</template>

<script setup>
import { computed } from 'vue';
import { urlFor } from '../sanity'; 
import { getImageDimensions } from '@sanity/asset-utils';

const props = defineProps({
  value: {
    type: Object,
    required: true,
  },
  isInline: { // This prop indicates if the image is inline with text
    type: Boolean,
    default: false,
  },
});

const imageUrl = computed(() => {
  // Use Sanity's getImageDimensions for responsive sizing/aspect ratio
  const { width, height } = getImageDimensions(props.value);
  
  return urlFor(props.value)
    .width(props.isInline ? 500 : width) // Example responsive width
    .height(props.isInline ? 200 : height)
    .fit('max')
    .auto('format')
    .url();
});
</script>


<style scoped>
img {
    border-radius: 5px;
}
img:hover {
    cursor: pointer;
}
</style>