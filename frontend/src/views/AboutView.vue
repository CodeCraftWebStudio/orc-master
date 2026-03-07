<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { marked } from 'marked';
import { useUserStore } from '@/stores/counter';
// https://www.youtube.com/shorts/ZYYnoxxLY7Q education is a scam
const isRegistered = ref(useUserStore().isRegistered);
const editAllowed = ref(true);
const redImageUrl = ref('../components/icons/RedCrossLogo.jpeg');
redImageUrl.value = 'data:image/jpeg;base64,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';
const sections = ref([
  {
    id: 'us',
    title: 'About Us',
    subsections: [
      {
        id: 'us-history',
        title: 'Our History',
        blocks: [
          { type: 'markdown', content: '## How we started\nWe began as a school Red Cross unit.' },
          { type: 'image', content: redImageUrl }
        ]
      }
    ]
  },
  {
    id: 'we',
    title: 'About the Red Cross',
    subsections: [
      {
        id: 'we-mission',
        title: 'Mission & Ideology',
        blocks: [
          { type: 'markdown', content: '**Humanity, neutrality, and service** guide our actions.' }
        ]
      }
    ]
  }
])

const activeSection = ref(null)

function onScroll() {
  const allTargets = document.querySelectorAll('[data-spy]')

  for (const el of allTargets) {
    const rect = el.getBoundingClientRect()
    if (rect.top <= 140 && rect.bottom >= 140) {
      activeSection.value = el.dataset.spy
      break
    }
  }
}


onMounted(() => {
  window.addEventListener('scroll', onScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
function addSubsection(sectionId) {
  const section = sections.value.find(s => s.id === sectionId)
  if (!section) return

  section.subsections.push({
    id: crypto.randomUUID(),
    title: 'New Subsection',
    blocks: [
      { type: 'markdown', content: 'Start writing here...' }
    ]
  })
}

</script>

<template>
<div class="about-page">
    <!-- Sidebar -->
<aside class="about-sidebar">
  <nav>
    <div v-for="section in sections" :key="section.id">
      <button
        :class="{ active: activeSection === section.id }"
        @click="document.getElementById (section.id)?.scrollIntoView({ behavior: 'smooth' })"
      >
        {{ section.title }}
      </button>

      <div class="sub-nav">
        <button
          v-for="sub in section.subsections"
          :key="sub.id"
          class="sub-button"
          :class="{ active: activeSection === sub.id }"
          @click="document.getElementById(sub.id)?.scrollIntoView({ behavior: 'smooth' })"
        >
          {{ sub.title }}
        </button>
      </div>
    </div>
  </nav>
</aside>


<main class="about-content">
  <section
    v-for="section in sections"
    :key="section.id"
    :id="section.id"
    :data-spy="section.id"
    class="about-section"
  >
    <h1 :contenteditable="editAllowed">{{ section.title }}</h1>

    <article
      v-for="sub in section.subsections"
      :key="sub.id"
      :id="sub.id"
      :data-spy="sub.id"
      class="about-subsection"
    >
      <h2 :contenteditable="editAllowed">{{ sub.title }}</h2>

      <div
        v-for="(block, i) in sub.blocks"
        :key="i"
        class="content-block"
      >
        <!-- Markdown -->
        <div
          v-if="block.type === 'markdown'"
          contenteditable="true"
          v-html="marked(block.content)"
          @input="block.content = $event.target.innerText"
        />

        <!-- Image -->
        <img
          v-if="block.type === 'image'"
          :src="block.content"
          class="about-image"
        />
      </div>
    </article>
  </section>
</main>

  </div>
</template>


<style>
/* =======================
   ABOUT PAGE LAYOUT
======================= */

.about-page {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
  max-width: 100vw;
  background: var(--color-background);
}

/* Sidebar */
.about-sidebar {
  position: sticky;
  top: 72px;
  height: calc(100vh - 72px);
  background: linear-gradient(
    180deg,
    #b30000,
    #e10600
  );
  padding: 1rem;
}

.about-sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.about-sidebar button {
  text-align: left;
  padding: 0.75rem 1rem;
  color: white;
  border-radius: 10px;
  background: transparent;
  font-weight: 500;
  transition: background 0.25s, transform 0.15s;
}

.about-sidebar button:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(4px);
}

.about-sidebar button.active {
  background: rgba(255, 255, 255, 0.25);
  box-shadow: inset 3px 0 white;
}

/* Content */
.about-content {
  padding: 3rem clamp(1.5rem, 5vw, 4rem);
  display: flex;
  flex-direction: column;
  gap: 5rem;
}

/* Sections */
.about-section {
  max-width: 900px;
  outline: none;
}

.about-section h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--rc-red);
  margin-bottom: 0.75rem;
}

.about-section p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--color-text);
}

/* Editable hint */
.about-section[contenteditable="true"]:focus {
  outline: 2px dashed var(--rc-red-soft);
  padding: 0.5rem;
  border-radius: 10px;
}

/* Mobile */
@media (max-width: 768px) {
  .about-page {
    grid-template-columns: 1fr;
  }

  .about-sidebar {
    position: relative;
    height: auto;
    top: 0;
  }

}
.about-subsection {
  margin-top: 2.5rem;
}

.about-subsection h2 {
  font-size: 1.4rem;
  color: var(--rc-red);
  margin-bottom: 0.75rem;
}

.sub-nav {
  margin-left: 0.75rem;
  display: flex;
  flex-direction: column;
}

.sub-button {
  font-size: 0.9rem;
  opacity: 0.85;
  padding-left: 1.25rem;
}

.sub-button.active {
  opacity: 1;
  text-decoration: underline;
}

.content-block {
  margin-bottom: 1.2rem;
}

.about-image {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}


</style>
