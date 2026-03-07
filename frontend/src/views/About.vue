<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { fetchAboutPage } from '@/sanity'
import { PortableText } from '@portabletext/vue'
import { myPortableTextComponents } from '@/portableTextComponents'
const page = ref(null);
const loading = ref(true);
const activeSection = ref(null);
let observer = null;
 
onMounted(async () => {
  try {
    const result = await fetchAboutPage()
    for (let item of result) {
      if (item.title == "About Us") {
        page.value = item;
      }
    }
    // page.value = result.find('About Us') || result[0];
    for (let section of page.value.sections) {
      console.log(`Section: ${section}, Section body: ${section.body}`);
      console.log('Section', section);
      console.log('Section body', section.body)
      console.log('Section keys', Object.keys(section))
    }
  await nextTick()
  const sections = document.querySelectorAll('.about-section')

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          activeSection.value = entry.target.id
        }
      })
    },
    {
      root: null,
      rootMargin: '-40% 0px -55% 0px',
      threshold: 0
    }
  )

  sections.forEach(section => observer.observe(section))
  if (entry.isIntersecting) {
  entry.target.classList.add('visible')
  activeSection.value = entry.target.id
}

  } catch (err) {
    console.error('Sanity error:', err)
  } finally {
    loading.value = false
  }
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>
<template>
  <div class="about-page">
    <!-- Loading -->
    <div v-if="loading" class="load">
      <div class="neo-spinner">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <p class="loading-text">Initializing neural archive…</p>
    </div>


    <!-- Sidebar -->
    <aside v-if="page" class="about-sidebar">
      <button
        v-for="section in page.sections"
        :key="section._key"
        :class="{ active: activeSection === section._key }"
      >
        <a :href="`#${section._key}`">{{ section.title }}</a>
      </button>
    </aside>

    <!-- Content -->
    <main v-if="page" class="about-content">
      <h1 class="text-red-700 text-4xl items-center justify-center">{{ page.title }}</h1>

      <section
        v-for="section in page.sections"
        :key="section._key"
        class="about-section"
        :id="section._key"
      >
        <h2>{{ section.title }}</h2>
         
        <!-- THIS NOW WORKS -->
        <PortableText v-if="section.blocks && section.blocks.length" :value="section.blocks" class="text-blue-300" :components="myPortableTextComponents"/>
      </section>
    </main>
  </div>
</template>
<style scoped>
button:hover {
  cursor: pointer;
}
.about-page {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
}

.load {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.about-sidebar {
  grid-column: 1;
  background: linear-gradient(180deg, #b30000, #e10600);
  padding: 2rem 1rem;
}

.about-content {
  grid-column: 2;
  padding: 3rem 2rem;
}

.about-content p {
  line-height: 1.6;
  margin-bottom: 1rem;
}





/* =======================
   FUTURISTIC LOADING
======================= */

.load {
  grid-column: 1 / -1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  justify-content: center;
  align-items: center;
  background: #000;
}

.neo-spinner {
  position: relative;
  width: 64px;
  height: 64px;
}

.neo-spinner span {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: #ff2a2a;
  animation: spin 1.2s linear infinite;
}

.neo-spinner span:nth-child(2) {
  inset: 6px;
  border-top-color: #ff6a6a;
  animation-duration: 1.6s;
}

.neo-spinner span:nth-child(3) {
  inset: 12px;
  border-top-color: #ffffff;
  animation-duration: 2s;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 0.95rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.75);
}
.about-sidebar {
  position: sticky;
  top: 72px;
  height: calc(100vh - 72px);
  padding: 1.25rem;
  background: linear-gradient(180deg, #b30000, #e10600);
  box-shadow: inset -1px 0 rgba(255,255,255,0.15);
}

.about-sidebar button {
  width: 100%;
  text-align: left;
  padding: 0.75rem 1rem;
  color: white;
  border-radius: 12px;
  font-weight: 500;
  backdrop-filter: blur(6px);
  transition:
    background 0.25s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.about-sidebar button:hover {
  background: rgba(255,255,255,0.18);
  transform: translateX(6px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.25);
  cursor: pointer;
}
.about-sidebar button.active {
  background: rgba(255,255,255,0.25);
  box-shadow: 0 8px 25px rgba(0,0,0,0.35);
  transform: translateX(10px);
}

.about-content {
  padding: 3rem clamp(1.5rem, 6vw, 4rem);
  display: flex;
  flex-direction: column;
  gap: 4.5rem;
  /* background: linear-gradient(180deg, #0a0a0a, #111); */
  background: white;
}

.about-content h1 {
  font-size: clamp(2.2rem, 5vw, 3rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #ff2a2a;
}

.about-section h2 {
  font-size: 1.6rem;
  margin-bottom: 0.75rem;
  color: #ff4d4d;
}

.about-content p {
  font-size: 1.05rem;
  line-height: 1.75;
  color: rgba(255,255,255,0.85);
}


.about-section :deep(p) {
  margin-bottom: 1.2rem;
}

.about-section :deep(h3) {
  font-size: 1.25rem;
  margin: 2rem 0 0.75rem;
  color: #ff6a6a;
}

.about-section :deep(a) {
  color: #ff8a8a;
  text-decoration: underline;
}

.about-section :deep(ul) {
  padding-left: 1.5rem;
  margin-bottom: 1.2rem;
}
aside button {
    border-bottom: 1px solid rgba(0,0,0,0.08);
}
.about-section {
  padding-bottom: 3rem;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.about-sidebar::after {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  width: 3px;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(255,255,255,0.4),
    transparent
  );
}
.about-sidebar button:focus-visible {
  outline: 2px solid white;
  outline-offset: 2px;
}

</style>