<script setup>
import { ref, onMounted } from 'vue'
import { useApiStore } from '@/stores/counter'

const contacts = ref([])
const api = useApiStore()
const emit = defineEmits(['openChat'])
const userData = ref('');
const userRole = ref('');
const bannedTypes = ref(['guest', 'member']);
const selectedRoom = ref('global');
const groupStyle = ref('');

async function getUsername() {
  console.log("Finding the user's name now...");
  const detailsRoute = '/api/user/getUserDetails';
  const data = await  api.apiFetch(detailsRoute, 'POST', {});
  return data;
}

onMounted(async () => {
  contacts.value = await api.apiFetch('/api/chat/getUsers');
  userData.value = await getUsername();
  userRole.value = userData.value.role_type;
  console.log('UserData keys: ');
  console.log(Object.keys(userData.value));
  contacts.value = contacts.value.filter(
  c => c.id !== userData.value.id
)
})

function openChat(roomname) {
  selectedRoom.value = roomname;
  emit('openChat', roomname)
}
async function openPrivateChat(contact) {
  const response = await api.apiFetch(
    `/api/chat/getPrivateRoom/${contact.id}`,
    'POST',
    {}
  )

  selectedRoom.value = response.room_name
  emit('openChat', response.room_name)
}
</script>

<template>
  <aside class="h-full flex flex-col bg-white md:flex">

    <div class="px-6 py-5 border-b bg-gray-50">
      <h2 class="text-2xl font-semibold text-gray-700">
        Contact List
      </h2>
    </div>

    <div class="flex-1 overflow-y-auto p-4 space-y-2">
    <button @click="openChat('global')" :class="[selectedRoom == 'global'   
                                                  ? groupStyle
                                                  : 'hover:bg-blue-50 hover:text-blue-600 w-full text-left px-4 py-3 rounded-lg transition flex items-center justify-between'
     ]">Global Chat</button>
     <br/>
     <br/>
         <button 
      v-if="userRole && !bannedTypes.includes(userRole.toLowerCase())"
      @click="openChat('executives')" :class="[selectedRoom == 'executive'   
                                                    ? groupStyle
                                                    : 'hover:bg-blue-50 hover:text-blue-600 w-full text-left px-4 py-3 rounded-lg transition flex items-center justify-between' 
       ]">
      Executive Room
    </button>
    <br/>
    <br/>
      <button
        v-for="contact in contacts"
        :key="contact.id"
        @click="openPrivateChat(contact)"
        :class="[
  'w-full text-left px-4 py-3 rounded-lg transition flex items-center justify-between',
  selectedRoom === contact.username
    ? 'bg-green-500 text-white shadow'
    : 'hover:bg-blue-50 hover:text-blue-600'
]"      >
        <span class="font-medium">
          {{ contact.username }}
        </span>

        <span class="w-2 h-2 bg-green-500 rounded-full"></span>
      </button>
    </div>

  </aside>
</template> 