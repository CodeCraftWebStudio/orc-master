<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import TopNotification from './components/TopNotification.vue'
import { useUserStore, useBaseURL, useApiStore } from './stores/counter'
import Error from './components/Error.vue'


const router = useRouter()
const userStore = useUserStore()
const apiStore = useApiStore()
const officialRegistration = ref(false);
const notification = ref(null)
const notificationDismissed = ref(false)
const isErrorPresent = ref(null);
const errorMessageDismissed = ref(false);
const errorMessage = ref(null);


function checkKey() {
  return !!localStorage.getItem('key')
}

function setKey(data) {
  if (data?.new_key) {
    localStorage.setItem('key', data.new_key)
  } else if (data) {
    localStorage.setItem('key', data)
  }
}

async function startSession() {
  const ROUTE_URL = useBaseURL().getBaseURL() + '/api/user/start'
  const res = await fetch(ROUTE_URL, {
    method: 'POST',
    credentials: 'include', 
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'Anonymous',
      class: 'Unassigned'
    })
  })
  const data = await res.json()
  setKey(data.session_key);
} 

function registrationNotification() {
  if (userStore.isRegistered || notificationDismissed.value) return

  notification.value = {
    message: 'It seems you have not yet joined the community',
    actions: [
      {
        label: 'Join Us',
        onClick: () => router.push('/register')
      }
    ]
  }
}

function closeNotification() {
  notification.value = null
  notificationDismissed.value = true
}
function logOutWarningNotification() {
  print("Log out warning notification has started.");
}
function showError(error_message) {
  errorMessage.value = error_message;
  errorMessageDismissed.value = false;
}
function hideError() {
  errorMessageDismissed.value = true;
  errorMessage.value = null;
}
// https://www.youtube.com/shorts/8S5PwW5hgEQ?feature=share
// https://www.youtube.com/shorts/MDvUUZd9RRA?feature=share
// https://www.youtube.com/shorts/o7xUwxQEG_Q?feature=share

onMounted(async () => {
  localStorage.clear()
  if (localStorage.length === 0 && !sessionStorage.getItem('reloaded')) {
    sessionStorage.setItem('reloaded', 'true');
    window.location.reload();
}
  isErrorPresent.value = localStorage.getItem('isErrorPresent') || false;
  if (checkKey()) {
    userStore.isRegistered = true
  } else {
    await startSession()
  }
  if (apiStore.sessionKey && checkKey()) {
    officialRegistration.value = await userStore.getUserIsRegistered();
  }
  if (localStorage.getItem('isErrorPresent') == true) {
    showError(localStorage.getItem('errorMsg'));
  }
  //registrationNotification()
})
</script>

<template>
  <div class="app-root">
    <div class="erros">
      <Error :message="errorMessage" @close="hideError" />
    </div>
    <header class="navbar">
      <RouterLink to="/">Home</RouterLink>
      <!-- <RouterLink to="/about">About</RouterLink> -->
      <RouterLink to="/aboutcms">About</RouterLink>
      <RouterLink to="/members">Events</RouterLink>
      <RouterLink to="/learn">Courses</RouterLink>
      <!-- <RouterLink to="/chatroom">Chatroom</RouterLink> -->
      <RouterLink to="contactus">Contact Us </RouterLink>

      <RouterLink
        v-if="!officialRegistration"
        class="cta"
        to="/register"
      >
        Register
      </RouterLink>
      <RouterLink
        v-if="officialRegistration"
        class="cta"
        to="/logout"
        @click="logOutWarningNotification"
      >
        Log Out
      </RouterLink>      
      <!-- To log out, I should probably just use localStorage.clear() and render their user inactive in the db (So that they can access it later somehow maybe via a password they can set in Members & Events) -->
    </header>

    <TopNotification
      v-if="notification"
      :message="notification.message"
      :action="notification.actions"
      @close="closeNotification"
    />


    <RouterView />
  </div>
</template>

<style>
.app-root {
  min-height: 100vh;
  background: #ffffff;
  color: #1a1a1a;
  font-family: "Inter", system-ui, sans-serif;
  z-index: 1000;
}

/* NAVBAR */
.navbar {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  justify-content: center;
  height: 80px;
  background: #c8102e; /* Red Cross Red */
  color: white;
}

.navbar a {
  color: white;
  text-decoration: none;
  font-weight: 600;
}

.navbar a:hover {
  text-decoration: underline;
}

/* CALL TO ACTION */
.cta {
  background: white;
  color: #c8102e !important;
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  font-weight: bold;
}

</style>