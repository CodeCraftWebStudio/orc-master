<script setup>
import ChatSidebar from '@/components/ChatSidebar.vue'
import ChatWindow from '@/components/ChatWindow.vue'
import { ref, onMounted } from 'vue'
import { useApiStore } from '../stores/counter.js'
 
const apiStore = useApiStore();
async function getUsername() {
  console.log("Finding the user's name now...");
  const detailsRoute = '/api/user/getUserDetails';
  const data = await  apiStore.apiFetch(detailsRoute, 'POST', {});
  return data;
}
const userId = ref(null);   // replace with real logged-in user id
const props = ref({});
const user_role = ref(null);
const showChat = ref(true);
const chatWindowStyle = ref('flex-1');
const chatSidebarStyle = ref('hidden md:block w-80 border-r border-slate-300 bg-white shadow-lg');
const currentRoom = ref(props.room || 'global')   // ADD THIS

onMounted(async() => {
    const user = await getUsername();
    userId.value = user.id;
    user_role.value = user.role_type.toLowerCase();
    props.value.room = 'global';
})
</script>

<template>
  <div 
    v-if="user_role !== 'guest'"
    class="flex h-screen bg-linear-to-br from-slate-100 to-slate-200"
  >
    <ChatSidebar 
      :class="chatSidebarStyle"
      @openChat="(roomName) => currentRoom = roomName" 
    />

    <div class="flex-1 flex">
      <ChatWindow 
        v-if="showChat" 
        :userId="userId"
        :room="currentRoom" 
        :class="chatWindowStyle"
      />
    </div>
  </div>

  <!-- Guest State -->
  <div 
    v-else 
    class="flex items-center justify-center h-screen bg-linear-to-br from-red-100 to-red-200"
  >
    <div class="bg-white shadow-xl rounded-2xl p-12 text-center max-w-xl">
      <h1 class="text-4xl font-bold text-red-700 mb-4">
        Access Restricted
      </h1>
      <p class="text-lg text-gray-700">
        It appears that you haven't registered. <br />
        Only members of the <span class="font-semibold text-red-600">ORC</span> can access the chat.
      </p>
    </div>
  </div>
</template>
<style scoped>
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.2);
  border-radius: 3px;
}
</style>  