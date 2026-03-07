<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'

const props = defineProps(['Questions'])

/* ---------------------------------
   Parse Questions From Sanity
----------------------------------*/

const parsedQuestions = computed(() => {
  if (!props.Questions?.children) return []

  return props.Questions.children.map((qSection, index) => {
    const findSection = (title) =>
      qSection.children.find(s =>
        s.title.trim().toLowerCase() === title.toLowerCase()
      )

    const getText = (section) =>
      section?.blocks?.[0]?.children?.[0]?.text || ''

    return {
      id: qSection._key,
      number: index + 1,
      question: getText(findSection('Content')),
      options: {
        a: getText(findSection('a')),
        b: getText(findSection('b')),
        c: getText(findSection('c')),
        d: getText(findSection('d'))
      },
      answer: getText(findSection('answer')).trim().toLowerCase()
    }
  })
})

/* ---------------------------------
   Quiz State
----------------------------------*/

const currentQuestionIndex = ref(0)
const selectedAnswers = ref({})
const showResults = ref(false)

/* ---------------------------------
   Global Timer (10s × questions)
----------------------------------*/

const totalTime = computed(() => parsedQuestions.value.length * 10)
const timeLeft = ref(0)
let interval = null

const startTimer = () => {
  timeLeft.value = totalTime.value

  interval = setInterval(() => {
    timeLeft.value--

    if (timeLeft.value <= 0) {
      submitQuiz()
    }
  }, 1000)
}

const stopTimer = () => clearInterval(interval)

onMounted(() => {
  if (parsedQuestions.value.length) {
    startTimer()
  }
})

onUnmounted(() => stopTimer())

/* ---------------------------------
   Methods
----------------------------------*/

const selectAnswer = (key) => {
  selectedAnswers.value[currentQuestionIndex.value] = key
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < parsedQuestions.value.length - 1) {
    currentQuestionIndex.value++
  }
}

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const submitQuiz = () => {
  stopTimer()
  showResults.value = true
}

/* ---------------------------------
   Computed
----------------------------------*/

const currentQuestion = computed(() =>
  parsedQuestions.value[currentQuestionIndex.value]
)

const score = computed(() => {
  let correct = 0

  parsedQuestions.value.forEach((q, index) => {
    if (selectedAnswers.value[index] === q.answer) {
      correct++
    }
  })

  return correct
})

const percentageScore = computed(() =>
  parsedQuestions.value.length
    ? Math.round((score.value / parsedQuestions.value.length) * 100)
    : 0
)
</script>

<template>
<section>
  <div class="container">

    <div v-if="parsedQuestions.length === 0" class="loader"></div>

    <div v-else>

      <!-- QUIZ -->
      <div v-if="!showResults" class="quiz">

        <div class="header">
          <h2>
            Question {{ currentQuestion.number }} / {{ parsedQuestions.length }}
          </h2>
          <p>⏱ {{ timeLeft }}s</p>
        </div>

        <progress
          :value="timeLeft"
          :max="totalTime"
        />

        <!-- Animated Question Transition -->
        <transition name="slide-fade" mode="out-in">
          <div
            :key="currentQuestion.id"
            class="question"
          >
            <h3>{{ currentQuestion.question }}</h3>

            <div class="answers">
              <button
                v-for="(text, key) in currentQuestion.options"
                :key="key"
                class="answer"
                :class="{
                  active: selectedAnswers[currentQuestionIndex] === key
                }"
                @click="selectAnswer(key)"
              >
                <strong>{{ key }}.</strong> {{ text }}
              </button>
            </div>
          </div>
        </transition>

        <div style="margin-top: 25px;">
          <button @click="prevQuestion" :disabled="currentQuestionIndex === 0">
            Back
          </button>

          <button
            @click="nextQuestion"
            :disabled="currentQuestionIndex === parsedQuestions.length - 1"
          >
            Next
          </button>

          <button @click="submitQuiz">
            Submit Quiz
          </button>
        </div>

      </div>

      <!-- RESULTS -->
      <div v-else class="result-screen">

        <h2>Your Score: {{ percentageScore }}%</h2>
        <p>
          You got {{ score }} out of {{ parsedQuestions.length }} correct.
        </p>

        <ul>
          <li
            v-for="(q, index) in parsedQuestions"
            :key="q.id"
            :class="{
              correct: selectedAnswers[index] === q.answer,
              incorrect: selectedAnswers[index] !== q.answer
            }"
          >
            <b>Question {{ index + 1 }}:</b>
            {{ q.question }}

            <p>
              Your Answer:
              <strong>
                {{ selectedAnswers[index] || 'Not answered' }}
              </strong>
            </p>

            <p>
              Correct Answer:
              <strong>{{ q.answer }}</strong>
            </p>
          </li>
        </ul>

        <button @click="location.reload()">
          Try Again
        </button>

      </div>

    </div>
  </div>
</section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&display=swap');

/* Animation */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.35s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Answer highlight colors */
button.answer.correct {
  border-color: #7ef89b;
  background: rgba(126, 248, 155, 0.15);
}

button.answer.incorrect {
  border-color: #fa919c;
  background: rgba(250, 145, 156, 0.15);
}

:root {
  --primary-color: #fe6300;
  --primary-color-light: #ffaf15;
  --correct-color: #7ef89b;
  --incorrect-color: #fa919c;
  --dark-color: #212529;
  --light-color: #e9e9e9;
  --bg-color: #f8f9fa;
  --card-bg: #ffffff;
  --primary-gradient: linear-gradient(
    135deg,
    var(--primary-color),
    var(--primary-color-light)
  );
}

* {
  box-sizing: border-box;
  font-family: "Jost", sans-serif;
}

body {
  margin: 0;
  background: radial-gradient(
    circle at top,
    #ffffff,
    var(--bg-color)
  );
  color: var(--dark-color);
}

/* ---------- layout ---------- */
.container {
  max-width: 760px;
  width: 95%;
  margin: auto;
}

/* ---------- header ---------- */
header {
  background: linear-gradient(
    180deg,
    rgba(254, 99, 0, 0.08),
    transparent
  );
}

header .container {
  padding: 60px 0 40px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

header h1 {
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  font-weight: 500;
  letter-spacing: -0.02em;
  margin-bottom: 10px;
}

header p {
  font-size: 1.25rem;
  opacity: 0.75;
}

/* ---------- buttons ---------- */
button,
input {
  width: 100%;
  max-width: 420px;
  margin: 12px auto;
  min-height: 48px;
  padding: 0 18px;
  font-size: 18px;
  border-radius: 10px;
}

button {
  background: var(--primary-gradient);
  color: black;
  border: none;
  cursor: pointer;
  font-weight: 600;
  letter-spacing: 0.02em;
  box-shadow: 0 10px 25px rgba(254, 99, 0, 0.35);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(254, 99, 0, 0.45);
}

button:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  box-shadow: none;
}

/* Answer buttons */
button.answer {
  background: var(--card-bg);
  color: var(--dark-color);
  border: 2px solid var(--light-color);
  box-shadow: none;
}

button.answer:hover {
  background: #f1f3f5;
}

button.answer.active {
  border-color: var(--primary-color);
  background: rgba(254, 99, 0, 0.08);
}

/* ---------- quiz card ---------- */
section {
  padding: 40px 0;
}

.quiz {
  background: var(--card-bg);
  border-radius: 20px;
  padding: 40px;
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.08),
    0 5px 15px rgba(0, 0, 0, 0.05);
  animation: fadeUp 0.6s ease;
}

.quiz .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.quiz .header h2 {
  font-size: 28px;
  font-weight: 600;
}

.quiz .header p {
  font-size: 18px;
  opacity: 0.7;
}

/* ---------- progress ---------- */
progress {
  width: 100%;
  height: 14px;
  border-radius: 999px;
  overflow: hidden;
  border: none;
  background: var(--light-color);
}

progress::-webkit-progress-bar {
  background: var(--light-color);
}

progress::-webkit-progress-value {
  background: var(--primary-gradient);
}

progress::-moz-progress-bar {
  background: var(--primary-gradient);
}

/* ---------- questions ---------- */
.question {
  padding-top: 40px;
}

.question h3 {
  font-size: clamp(1.8rem, 4vw, 2.4rem);
  font-weight: 600;
  line-height: 1.3;
}

/* ---------- answers ---------- */
.answers {
  padding-top: 30px;
}

/* ---------- results ---------- */
.result-screen ul {
  padding: 0;
}

.result-screen li {
  background: var(--card-bg);
  margin: 20px auto;
  padding: 20px;
  max-width: 500px;
  border-radius: 16px;
  border: 2px solid var(--light-color);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
}

.result-screen li.correct {
  border-color: var(--correct-color);
  background: rgba(126, 248, 155, 0.08);
}

.result-screen li.incorrect {
  border-color: var(--incorrect-color);
  background: rgba(250, 145, 156, 0.08);
}

.result-screen li b {
  display: block;
  margin-bottom: 10px;
}

/* ---------- loader ---------- */
.loader {
  margin: 60px auto;
  width: 60px;
  aspect-ratio: 1;
  border-radius: 50%;
  background:
    radial-gradient(farthest-side, var(--primary-color) 94%, #0000) top/10px 10px no-repeat,
    conic-gradient(#0000 30%, var(--primary-color));
  -webkit-mask: radial-gradient(
    farthest-side,
    #0000 calc(100% - 10px),
    #000 0
  );
  animation: spin 1s infinite linear;
}

@keyframes spin {
  to {
    transform: rotate(1turn);
  }
}

/* ---------- animation ---------- */
@keyframes fadeUp {
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