<script setup>
import { fetchAboutPage as fetchPages} from '@/sanity';
import {ref, onMounted} from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const pages = ref(null);
onMounted(async () => {
    pages.value = await fetchPages();
    for (let item of pages.value) {
        if (item.title) {
        console.log("Title exists");
        if (item.title == "About Us") {
        pages.value.splice(pages.value.indexOf(item), 1); // One is the about page, the rest are educatonal artcles.
        }
        if (item.title == "Quiz") {
        pages.value.splice(pages.value.indexOf(item), 1); // One is the about page, the rest are educatonal artcles.
        }
        } else {
            console.log("Title doesn't exist");
            console.log(Object.keys(item))
        }

    } 
});
async function Read(id) {
    router.push(`/learn/article/${id}`)
}
</script>

<template>
    <div class="content">
        <aside class="left-0 bg-gray-100 text-xl sidebar">
            <div v-if="pages && pages.length" v-for="page in pages" :key="page._id">
                <button class="hover:text-blue-700" :id="page._id" @click="Read(page._id)"> {{ page.title }}</button>
            </div> 
        </aside>
    </div>
</template>

<style scoped>
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  padding: 1.5rem 1rem;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Buttons */
.sidebar button {
  width: 100%;
  text-align: left;
  padding: 0.6rem 0.75rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: #1f2937;
  background: transparent;
  border-radius: 8px;
  transition: background 0.2s ease, transform 0.15s ease;
}

.sidebar button:hover {
  background: royalblue;
  transform: translateX(4px);
  cursor: pointer;
  color: rgba(100, 0,  blue, alpha)
}

/* Mobile */
@media (max-width: 768px) {
  .sidebar {
    height: auto;
    flex-direction: row;
    overflow-x: auto;
    border-right: none;
    border-bottom: 1px solid royalblue;
  }

  .sidebar button {
    white-space: nowrap;
  }
}

</style>