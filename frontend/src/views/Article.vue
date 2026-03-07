<script setup>
import { fetchAboutPage as fetchPages } from '@/sanity'
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { PortableText } from '@portabletext/vue'
import { myPortableTextComponents } from '@/portableTextComponents'
import Challenge from './Challenge.vue'

/* ---------------- state ---------------- */
const route = useRoute()
const pages = ref([])
const page = ref(null)
const challenge = ref(false)
const activeSection = ref(null);
const quiz = ref({});
/* progress */
const currentStep = ref(1)
const totalSteps = 3

const progressPercent = computed(() =>
  ((currentStep.value - 1) / (totalSteps - 1)) * 100
)

/* ---------------- methods ---------------- */
// 8033092964
// Oladimeji
//https://wa.me/whatsappphonenumber?text=urlencodedtexT
/*
Example
To create a link to number 1 555-123-4567 with the pre-filled message "Hello, I am interested in your services", the URL is:
https://wa.me/15551234567?text=Hello%2C%20I%20am%20interested%20in%20your%20services
https://wa.me/2348033295843?text=I%would%like%to%ask%about%the%ORC
 */ 
const startChallenge = () => {
  challenge.value = true
}

const nextStep = () => {
  if (currentStep.value < totalSteps) currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--
}

/* ---------------- lifecycle ---------------- */
onMounted(async () => {
  pages.value = await fetchPages()
  page.value = pages.value.find(p => p._id === route.params.id)
  const Questions = page.value.sections.find(section => section.title == "Questions");
  quiz.value = Questions;
  console.log(Questions);
  const filteredSections = computed(() =>
  page.value?.sections?.filter(s => s.title !== "Questions") || []
  
)
  console.log(filteredSections);
})
</script>

<template>
  <!-- Progress Header -->
  <div v-if="page && !challenge" class="progress-wrapper">
    <div class="progress-track">
      <div
        class="progress-bar"
        :style="{ width: progressPercent + '%' }"
      />
      <div
        v-for="step in totalSteps"
        :key="step"
        class="progress-circle"
        :class="{ active: step <= currentStep }"
      >
        {{ step }}
      </div>
    </div>

    <div class="progress-buttons">
      <button @click="prevStep" :disabled="currentStep === 1">Back</button>
      <button @click="nextStep" :disabled="currentStep === totalSteps">
        Next
      </button>
    </div>
  </div>

  <!-- Page Content -->
  <div v-if="page && !challenge" class="page-container">
    <h1 class="page-title">{{ page.title }}</h1>
    
    <section
    v-for="section in page.sections"
    :key="section._key"
    class="content-section"
  >
    
    <h2
    v-if="section.title && section.title !== 'Questions' "
      class="section-title hover-title"
      @mouseenter="activeSection = section._key"
      @mouseleave="activeSection = null"
      @click="activeSection = section._key"
    >
      {{ section.title == 'Questions' ? '' : section.title }}
      <span class="hover-hint">hover to read</span>
    </h2>

    <transition name="reveal" v-if="section.title && section.title !== 'Questions'">
      <div
        v-if="activeSection === section._key"
        class="section-body"
      >
        <PortableText
          v-if="section.blocks && section.blocks.length"
          :value="section.blocks || section.body"
          class="portable-text"
          :components="myPortableTextComponents"
        />
      </div>
    </transition>
  </section>


    <button class="challenge-btn" @click="startChallenge">
      🚀 Challenge Yourself
    </button>
  </div>

  <!-- Challenge -->
  <Challenge v-if="challenge" :Questions="quiz"/>
</template>

<style scoped>
/* ---------- layout ---------- */
.page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  animation: fadeIn 0.6s ease;
}

.page-title {
  font-size: 3rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 3rem;
  background: linear-gradient(90deg, #60a5fa, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ---------- sections ---------- */
.content-section {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  transition: transform 0.3s ease;
}

.content-section:hover {
  transform: translateY(-4px);
}

.section-title {
  font-size: 1.75rem;
  color: #93c5fd;
  margin-bottom: 1rem;
}

.portable-text {
  color: #e0f2fe;
  line-height: 1.8;
}

/* ---------- challenge button ---------- */
.challenge-btn {
  display: block;
  margin: 4rem auto 0;
  padding: 1rem 3rem;
  font-size: 1.2rem;
  font-weight: 700;
  border-radius: 999px;
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  color: white;
  border: none;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(37, 99, 235, 0.5);
  transition: all 0.3s ease;
}

.challenge-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 15px 40px rgba(56, 189, 248, 0.7);
}

/* ---------- progress ---------- */
.progress-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0;
}

.progress-track {
  position: relative;
  width: 320px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-track::before {
  content: '';
  position: absolute;
  height: 4px;
  width: 100%;
  background: #1e293b;
  top: 50%;
  transform: translateY(-50%);
  z-index: 0;
}

.progress-bar {
  position: absolute;
  height: 4px;
  background: linear-gradient(90deg, #38bdf8, #2563eb);
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
  transition: width 0.4s ease;
}

.progress-circle {
  height: 36px;
  width: 36px;
  border-radius: 50%;
  background: #020617;
  border: 3px solid #1e293b;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  z-index: 2;
  transition: all 0.3s ease;
}

.progress-circle.active {
  border-color: #38bdf8;
  color: #e0f2fe;
  background: #020617;
}

.progress-buttons {
  margin-top: 1.5rem;
}

.progress-buttons button {
  margin: 0 0.5rem;
  padding: 0.5rem 1.5rem;
  border-radius: 999px;
  border: none;
  background: #1e40af;
  color: white;
  cursor: pointer;
}

.progress-buttons button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.section-body {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.15);
}

.portable-text {
  color: #e0f2fe;
  line-height: 1.85;
  font-size: 1.05rem;
}

/* Paragraphs */
.portable-text p {
  margin-bottom: 1.25rem;
}

/* Headings inside PortableText */
.portable-text h3,
.portable-text h4 {
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  color: #bae6fd;
  font-weight: 700;
}

/* Lists */
.portable-text ul,
.portable-text ol {
  padding-left: 1.5rem;
  margin-bottom: 1.5rem;
}

.portable-text li {
  margin-bottom: 0.5rem;
}

/* Quotes */
.portable-text blockquote {
  border-left: 3px solid #38bdf8;
  padding-left: 1rem;
  margin: 2rem 0;
  color: #bae6fd;
  font-style: italic;
  background: rgba(56, 189, 248, 0.05);
}

/* Links */
.portable-text a {
  color: #7dd3fc;
  text-decoration: underline;
  transition: color 0.3s ease;
}

.portable-text a:hover {
  color: #38bdf8;
}



.hover-title {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
}

.hover-hint {
  font-size: 0.75rem;
  opacity: 0;
  color: #7dd3fc;
  transition: opacity 0.3s ease;
}

.hover-title:hover .hover-hint {
  opacity: 1;
}

/* ---------- animation ---------- */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
