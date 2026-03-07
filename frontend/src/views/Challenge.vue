<script setup>
import { ref } from 'vue';
import StartScreen from '@/components/StartScreen.vue';

const props = defineProps(['Questions'])
const startQuiz = ref(false);
</script>

<template>
<div v-if="!startQuiz">
  <header><div class="container flex"><h1>Challenge Yourself By Taking a Quiz!</h1></div></header>
  <button @click="startQuiz = true" class="justify-center adjustment">Start Quiz</button>
</div>
<StartScreen v-if="startQuiz" :Questions="Questions"/>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&display=swap');

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
.adjustment {
  position: center;
  justify-content: center;
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