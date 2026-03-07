<script setup>

</script>

<template>
    <h2 class="text-blue-500 align-center justify-center">Interested in learning a few things? </h2>
    <section class="text-black starter">
        <p>The ORC Society believes that knowledge is one of the most powerful tools for protecting health and saving lives. Education should be accessible, clear, and available to everyone — regardless of location or circumstance. </p>
        <p>This page exists to share essential information, practical guidance, and reliable insights related to health, safety, and well-being. By providing this content digitally, we reduce the need for physical contact while ensuring that learning remains continuous and inclusive.</p>
        <p>Take your time, explore the topics, and learn at your own pace. Every piece of knowledge you gain here is meant to empower you to make safer, more informed decisions.</p>
    </section>
</template>

<style scoped>
h2 {
  font-size: clamp(1.6rem, 3.5vw, 2.2rem);
  font-weight: 700;
  color: #1e40af; /* calm blue */
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

section {
  max-width: 680px;
}

section p {
  font-size: 1.05rem;
  line-height: 1.75;
  color: #1f2937; /* neutral dark gray */
}

/* Optional subtle emphasis */
section p::before {
  content: '';
  display: block;
  width: 48px;
  height: 3px;
  background: #1e40af;
  margin-bottom: 1rem;
  border-radius: 2px;
}

/* Responsive spacing */
@media (max-width: 640px) {
  section p {
    font-size: 1rem;
  }
}
h2 {
  font-size: clamp(1.8rem, 4vw, 2.4rem);
  font-weight: 700;
  color: #1e40af;
  margin-bottom: 1.25rem;
}

section {
  max-width: 720px;
}

section p {
  font-size: 1.05rem;
  line-height: 1.75;
  color: #1f2937;
  margin-bottom: 1.1rem;
}

/* Remove repeated dividers */
section p::before {
  content: none;
}

/* Add a single divider instead */
section::before {
  content: '';
  display: block;
  width: 56px;
  height: 4px;
  background: #1e40af;
  margin-bottom: 1.25rem;
  border-radius: 2px;
}
.starter {
    margin-left: 15px;
}
</style>