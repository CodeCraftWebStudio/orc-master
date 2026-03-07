<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import { useApiStore } from '../stores/counter.js';

const apiStore = useApiStore();
const events = ref([])
const sidebarOpen = ref(false)
const selectedDate = ref(null)
const isAdmin = ref(false)
const settingsOpen = ref(false)

const weeklyMeeting = ref({
  enabled: false,
  weekday: 1,   // Monday (0 = Sun)
  time: '15:30'
})
watch(weeklyMeeting, async () => {
  await loadEvents()
}, { deep: true })

const form = ref({
  date: '',
  time: '',
  description: ''
})
async function getUsername() {
  console.log("Finding the user's name now...");
  const detailsRoute = '/api/user/getUserDetails';
  const data = await  apiStore.apiFetch(detailsRoute, 'POST', {});
  return data;
}

async function getUserIsAdmin() {
  // intentionally empty for now
  const data = await getUsername();
  if (data.role_type == "admin") return true;
  return false
}

async function loadEvents() {
  const rawEvents = await apiStore.apiFetch('/api/database/events', 'POST', {
    op: 'read'
  })

  const dbEvents = rawEvents.map(e => ({
    id: e.id,
    title: e.title,
    start: e.time_obj
      ? `${e.date_obj}T${e.time_obj}`
      : e.date_obj
  }))

  const today = new Date().toISOString().split('T')[0]
  const weeklyEvents = generateWeeklyMeetings(today)

  events.value = [...dbEvents, ...weeklyEvents]
}


function generateWeeklyMeetings(startDate, weeks = 12) {
  if (!weeklyMeeting.value.enabled) return []

  const results = []
  const base = new Date(startDate)

  for (let i = 0; i < weeks; i++) {
    const d = new Date(base)
    d.setDate(d.getDate() + i * 7)

    if (d.getDay() !== weeklyMeeting.value.weekday) {
      d.setDate(d.getDate() + ((7 + weeklyMeeting.value.weekday - d.getDay()) % 7))
    }

    const dateStr = d.toISOString().split('T')[0]

    results.push({
      id: `weekly-${dateStr}`,
      title: 'Weekly Meeting',
      start: `${dateStr}T${weeklyMeeting.value.time}`,
      editable: false,
      classNames: ['weekly-meeting']
    })
  }

  return results
}


const isWeekend = (dateStr) => {
  const day = new Date(dateStr).getDay()
  return day === 0 || day === 6
}

const isPastDate = (dateStr) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return new Date(dateStr) < today
}

const handleDateClick = (info) => {
  if (!isAdmin.value) return
  if (isWeekend(info.dateStr)) return
  if (isPastDate(info.dateStr)) return
  selectedDate.value = info.dateStr
  form.value = {
    date: info.dateStr,
    time: '',
    description: ''
  }
  sidebarOpen.value = true
}

const saveEvent = async () => {
  await apiStore.apiFetch('/api/database/events', 'POST', {
    op: 'create',
    date_obj: form.value.date,
    time_obj: form.value.time || null,
    description_obj: form.value.description
  })

  await loadEvents()
  sidebarOpen.value = false
}


const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  events: events.value,
  dateClick: handleDateClick,
  height: 'auto',
  dayCellClassNames(arg) {
    const day = arg.date.getDay()
    const today = new Date()
    today.setHours(0,0,0,0)

    let classes = []
    if (day === 0 || day === 6) classes.push('fc-weekend-disabled')
    if (arg.date < today) classes.push('fc-past-disabled')
    return classes
  }
}))

onMounted(async () => {
  isAdmin.value = await getUserIsAdmin();
  await loadEvents();
})

</script>

---

## 🧩 Template

```vue
<template>
  <div class="calendar-layout">
    <!-- Calendar -->
    <div class="calendar-wrapper">
      <FullCalendar
        :options="calendarOptions"
      />
    </div>
    <!----Left Settings Sidebar-->
    <button
    v-if="isAdmin"
    class="admin-settings-btn"
    @click="settingsOpen = true"
  >
    ⚙️ Admin Settings
    </button>
<aside :class="['settings-sidebar', { open: settingsOpen }]">
  <h2>Weekly Meeting</h2>

  <label class="toggle">
    <input type="checkbox" v-model="weeklyMeeting.enabled" />
    Enable weekly meetings
  </label>

  <div v-if="weeklyMeeting.enabled">
    <label>
      Day
      <select v-model="weeklyMeeting.weekday">
        <option :value="1">Monday</option>
        <option :value="2">Tuesday</option>
        <option :value="3">Wednesday</option>
        <option :value="4">Thursday</option>
        <option :value="5">Friday</option>
      </select>
    </label>

    <label>
      Time
      <input type="time" v-model="weeklyMeeting.time" />
    </label>
  </div>

  <button class="secondary" @click="settingsOpen = false">
    Close
  </button>
</aside>

    
    <!-- Sidebar -->
    <aside :class="['sidebar', { open: sidebarOpen }]">
      <h2>Schedule Event</h2>

      <div v-if="selectedDate" class="sidebar-content">
        <p class="date">{{ selectedDate }}</p>

        <label>
          Time
          <input type="time" v-model="form.time" />
        </label>

        <label>
          Description
          <textarea
            rows="4"
            placeholder="Event details..."
            v-model="form.description"
          />
        </label>

        <button @click="saveEvent">Save Event</button>
        <button class="secondary" @click="sidebarOpen = false">
          Cancel
        </button>
      </div>

      <p v-else class="empty">
        Select a weekday to schedule an event
      </p>
    </aside>
  </div>
</template>



<style scoped>
.calendar-layout {
  display: flex;
  position: relative;
  z-index: 1;
}

/* ---------- calendar ---------- */
.calendar-wrapper {
  flex: 1;
  padding: 1.5rem;
  z-index: 1;
}

/* Weekend, weekly meetings & past dates styling */
.fc-day-sat,
.fc-day-sun {
  background: rgba(239, 68, 68, 0.08);
  pointer-events: none;
  z-index: 1;
}

.fc-day-sat .fc-daygrid-day-number,
.fc-day-sun .fc-daygrid-day-number {
  color: #dc2626;
}

.fc-past-disabled {
  background: rgba(148, 163, 184, 0.08);
  pointer-events: none;
  opacity: 0.5;
}

.weekly-meeting {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: blue;
  border: none;
  z-index: 100000000000000000000000000000000000;
}



/* ---------- sidebar ---------- */
.sidebar {
  width: 340px;
  background: #020617;
  color: #e5e7eb;
  padding: 2rem;
  border-left: 1px solid rgba(148, 163, 184, 0.15);
  position: absolute;
  right: -360px;
  top: 0;
  height: 100%;
  transition: right 0.35s ease;
  z-index: 1000000000000000000000000000000000000000000000000000000000000000000000000000000000;
}

.sidebar.open {
  right: 0;
}

.sidebar h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.sidebar .date {
  font-weight: 600;
  margin-bottom: 1rem;
  color: #93c5fd;
}

.sidebar label {
  display: block;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.sidebar input,
.sidebar textarea {
  width: 100%;
  margin-top: 0.25rem;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #334155;
  background: #020617;
  color: #e5e7eb;
}

.sidebar button {
  width: 100%;
  margin-top: 0.75rem;
  padding: 0.6rem;
  border-radius: 999px;
  border: none;
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  color: white;
  cursor: pointer;
}

.sidebar button.secondary {
  background: transparent;
  border: 1px solid #334155;
}


/*----- Left Sidebar -----*/
.settings-sidebar {
  width: 320px;
  background: white;
  color: blue;
  padding: 2rem;
  position: absolute;
  left: -340px;
  top: 0;
  height: 100%;
  transition: left 0.35s ease;
  z-index: 100000000000000000000000000;
  border-right: 1px solid rgba(148, 163, 184, 0.15);
}

.settings-sidebar.open {
  left: 0;
}

.admin-settings-btn {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 60;
}

.empty {
  opacity: 0.6;
  font-size: 0.9rem;
}

/* ---------- polish ---------- */
.fc {
  --fc-border-color: rgba(148, 163, 184, 0.15);
  --fc-today-bg-color: rgba(56, 189, 248, 0.15);
}
</style>
