<script setup>
import {ref, onMounted} from 'vue';
const images = ref(null);
const currentImage = ref(null);
const currentImageNumber = ref(0);
const lengthOfShowTime = ref(2);
const maxImageNumber = ref(10);
let array = [1, 2, 3, 4, 4, 5, 6, 7];

onMounted(async() => {
    // Go to a folder of images and select the 10 latest. Anything less recent should be deleted upon checking this
    images.value = images.value.slice(0, maxImageNumber.value);
    while (true) {
    setTimeout(() => {
        currentImage.value = images[currentImageNumber];
        currentImageNumber++;
    }, lengthOfShowTime.value * 1000 );
    }

})
</script>


<template>
    <h1 class="text-black text-2xl justify-center align-center">Recent Events</h1>
    <div id="eventSlideshow">
        <img src="" alt="Our recent events" id="event">
    </div>
</template>

<style scoped>

</style>