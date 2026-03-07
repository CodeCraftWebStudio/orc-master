<script setup>
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from '../stores/counter.js';
import { useApiStore } from '../stores/counter.js';
import { RouterLink } from 'vue-router';


const apiStore = useApiStore();
const userStore = useUserStore();
const name = ref(null)
const role = ref(null);
const color = ref(null);
const avatarUrl = ref(localStorage.getItem('avatar_url'))
const role_title = ref(null);
const officialRegistration = userStore.getUserIsRegistered();
const initial = computed(() =>
  name.value ? name.value[0].toUpperCase() : '?'
)

  
async function getUsername() {
  console.log("Finding the user's name now...");
  const detailsRoute = '/api/user/getUserDetails';
  const data = await  apiStore.apiFetch(detailsRoute, 'POST', {});
  return data;
}
onMounted(async () => {
  if (!userStore.getUserIsRegistered()) {
    console.log("User is not registered");
     return;
}
  const data = await getUsername();
  const values = {
    name: data.name,
    role: data.role_type,
    title: data.role_title,
}
  if (!values || !values.name || !values.role) {
    console.log("Unsuccessful call");
    return;
  }
  if (values.role.toLowerCase == "member") {
    console.log("Ok user is just a member")
    return;
}
  name.value = values.name;
  role.value = values.role;
  const colour_map = {
    'member': 'teal',
    'non_editor_exec': 'purple',
    'editing_exec': 'blue',
    'admin': 'red'
}
  color.value = colour_map[role.value];

})
function setAvatarUrl(e) {
  avatarUrl.value = e.target.value
  localStorage.setItem('avatar_url', avatarUrl.value)
}

</script>

<template>
<div class="content relative">
    <!-- <h1 class="welcome-title" v-if="role && name">Welcome, {{  role_title ||   '' }} {{ role }} {{ name }}</h1>  (It was just for debugging)-->
      <!-- <RouterLink to="/profile"> -->
        <div class="user-controls justify-end" v-if="officialRegistration">
          <div class="relative inline-block user-icon justify-end group" v-if="officialRegistration">
          <!-- Avatar -->
          <div
            class="avatar w-16 h-16 rounded-full flex items-center justify-center text-xl font-semibold text-gray-700 cursor-pointer transition-transform transform hover:scale-105"
            :style="{ background: color || '#c8102e' }"
            v-if="officialRegistration"
          >
              <img v-if="avatarUrl" :src="avatarUrl" class="w-full h-full rounded-full object-cover" />
                <span v-else>{{ initial || 'A' }}</span>
          </div>

          <!-- Tooltip (hidden by default, appears on hover) -->
          <div
            class="absolute right-0 mt-3 p-4 w-64 bg-white text-gray-800 rounded-xl shadow-xl opacity-0 pointer-events-none transition-all duration-200 group-hover:opacity-100 group-hover:pointer-events-auto"
          >
            <label class="block mb-2 text-sm font-medium">Upload Avatar</label>
            <input
              type="file"
              @change="uploadAvatar"
              class="w-full text-sm text-gray-700 border border-gray-300 rounded px-2 py-1 mb-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />

            <label class="block mb-2 text-sm font-medium">Image URL</label>
            <input
              type="text"
              placeholder="Paste image URL"
              @change="setAvatarUrl"
              class="w-full text-sm text-gray-700 border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
        </div>
      </div>
    <!-- </RouterLink> -->
    <section class="welcome">
      <div class="welcome-card">
        <h1 class="welcome-title">
          Welcome to the OAUIS Red Cross Society
        </h1>

        <p class="welcome-subtitle">
          Nigerian Red Cross Society <br />
          Obafemi Awolowo University International School, Ile-Ife
        </p>

        <div class="welcome-divider"></div>

        <div class="welcome-content">
          <p>
            We are part of the Nigerian Red Cross Society, committed to
            humanitarian service, compassion, and the protection of human life
            and dignity.
          </p>

          <p>
            At OAUIS, our Red Cross Society empowers students to serve their
            community through first aid, health awareness, emergency response,
            and volunteerism.
          </p>

          <p>
            This platform is designed to keep members informed, connected, and
            actively involved in our activities, trainings, and outreach
            programs.
          </p>
          <p>
            So now you know, we're not just some high school club. We're an organization that steps in to help because it counts. We're a family that cares. 
          </p>
          <p v-if="officialRegistration"><RouterLink to="/register"><button class="cta">Join Us</button></RouterLink></p><p v-if="!officialRegistration"><button class="cta">Joined</button></p>
        </div>

        <div class="welcome-motto">
          <span>Humanity</span>
          <span>•</span>
          <span>Service</span>
          <span>•</span>
          <span>Compassion</span>
        </div>
      </div>
    </section>
</div>
</template>

<style scoped>
/* ROOT */
:root {
  --adminBackground: red;
  --editingExecBackground: blue;
  --nonEditingExecBackground: purple;
  --memberBackground: teal;
  --circleRadius: 50px;
}
/* PAGE BACKGROUND */
.welcome {
  min-height: calc(100vh - 80px);
  display: flex;
  justify-content: center;
  align-items: center;
  background: #ffffff;
  padding: 2rem 1rem;
}

/* CARD */
.welcome-card {
  max-width: 850px;
  background: #fdfdfd;
  border-radius: 12px;
  padding: 3rem 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
  text-align: center;
}

/* TITLE */
.welcome-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #c8102e; /* Red Cross Red */
  margin-bottom: 0.5rem;
}

/* SUBTITLE */
.welcome-subtitle {
  font-size: 1rem;
  color: #555;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

/* DIVIDER */
.welcome-divider {
  width: 80px;
  height: 4px;
  background: #c8102e;
  margin: 1.5rem auto;
  border-radius: 2px;
}

/* CONTENT */
.welcome-content p {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #333;
  margin-bottom: 1rem;
}

/* MOTTO */
.welcome-motto {
  margin-top: 2rem;
  font-weight: 600;
  color: #c8102e;
  display: flex;
  justify-content: center;
  gap: 0.6rem;
  flex-wrap: wrap;
  font-size: 0.95rem;
}
/* CALL TO ACTION */
.cta {
  background: white;
  color: #c8102e !important;
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}
.avatar {
  border-radius: 50%;
}
.avatar {
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.user-controls {
  position: fixed;
  top: 20px;
  right: 30px;
  z-index: 1000;
}
.content {
  position: relative;
  width: 100%;
}
</style>
