 <script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useApiStore } from '@/stores/counter'
import socket from '@/socket'

const props = defineProps(['userId', 'room'])
 
// --- state
const api = useApiStore()
const messages = ref([])
const newMessage = ref('')
const typingUsers = ref([])
const unreadCount = ref(0)

// Default session key
const sessionKey = localStorage.getItem('key')

// --- Helpers
function joinRoom(roomName) {
  if (!roomName) roomName = 'global'  // ✅ default to global
  socket.emit("join", {
    session_key: sessionKey,
    room: roomName
  })
}

function leaveRoom(roomName) {
  if (!roomName) roomName = 'global'
  socket.emit("leave", {
    session_key: sessionKey,
    room: roomName
  })
}

async function loadMessages(roomName) {
  if (!roomName) roomName = 'global'
  const roomRes = await api.apiFetch(`/api/chat/getRoom/${roomName}`)
  if (!roomRes.room_id) return
  const msgs = await api.apiFetch(`/api/chat/getMessages/${roomRes.room_id}`)
  messages.value = msgs
}

function sendMessage() {
  if (!newMessage.value.trim()) return

  socket.emit("send_message", {
    content: newMessage.value,
    session_key: sessionKey,
    room: props.room || 'global'
  })

  newMessage.value = ''
}

function sendTyping(state) {
  socket.emit("typing", {
    session_key: sessionKey,
    room: props.room || 'global',
    typing: state
  })
}

// --- Lifecycle
onMounted(() => {
  const roomToJoin = props.room || 'global'  // ✅ ensure a valid room
  joinRoom(roomToJoin)
  loadMessages(roomToJoin)

  socket.on("receive_message", (msg) => {
    if ((msg.room || 'global') === roomToJoin) {
      messages.value.push(msg)
    } else {
      unreadCount.value++
    }
  })

  socket.on("user_typing", (data) => {
    typingUsers.value = data.typing ? [data.username] : []
  })
})

// --- Watch for room changes
watch(() => props.room, async (newRoom, oldRoom) => {
  const oldRoomName = oldRoom || 'global'
  const newRoomName = newRoom || 'global'

  if (oldRoomName) leaveRoom(oldRoomName)

  messages.value = []
  unreadCount.value = 0

  joinRoom(newRoomName)
  await loadMessages(newRoomName)
})

// --- Cleanup
onUnmounted(() => {
  socket.off("receive_message")
  socket.off("user_typing")
})
</script>
<template>
  <div class="flex flex-col h-full bg-white">

    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h2 class="text-xl font-semibold text-gray-700">
        {{
            room.startsWith('private_')
            ? 'Private Chat'
            : room === 'global'
                ? 'Global Chat'
                : 'Executive Room'
        }}
        </h2>
    </div>

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto px-6 py-4 space-y-3 bg-gray-100">
      <div 
        v-for="msg in messages" 
        :key="msg.id"
        :class="[
          'max-w-lg px-4 py-2 rounded-xl shadow-sm transition-all duration-300 ease-in-out',
          msg.user_id === userId
            ? 'bg-blue-600 text-white ml-auto'
            : 'bg-white text-gray-800'
        ]"
      >
        <div class="text-sm font-semibold mb-1">
          {{ msg.username }}
        </div>
        <div>{{ msg.content }}</div>
        <div class="text-xs opacity-70 mt-1">
          {{ msg.status }}
        </div>
      </div>
    </div>

    <!-- Typing Indicator -->
    <div 
      v-if="typingUsers.length"
      class="px-6 py-2 text-sm text-gray-500 italic"
    >
    {{ typingUsers.join(', ') }} is typing... 
    </div>

    <!-- Unread -->
    <div 
      v-if="unreadCount > 0"
      class="px-6 py-1 text-xs text-blue-600 font-medium"
    >
      {{ unreadCount }} new messages
    </div>

    <!-- Input Area -->
    <div class="flex items-center gap-3 p-4 border-t bg-white">
      <input 
        @keyup.enter="sendMessage"
        v-model="newMessage"
        @input="sendTyping(true)"
        @blur="sendTyping(false)"
        placeholder="Type your message..."
        class="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
      />

      <button 
        @click="sendMessage"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-full shadow-md transition transform hover:scale-105"
      >
        Send
      </button>
    </div>

  </div>
</template>   