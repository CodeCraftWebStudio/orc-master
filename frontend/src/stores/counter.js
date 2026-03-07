import { defineStore } from 'pinia'
import { ref } from 'vue'
 
/* =========================
   Constants
========================= */
const BASE_URL = 'http://localhost:5000'
const JSON_HEADERS = { 'Content-Type': 'application/json' }
const CREDENTIALS = 'include'
const ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

/* =========================
   Base URL Store
========================= */
export const useBaseURL = defineStore('baseURL', () => {
  const baseURL = BASE_URL

  function getBaseURL() {
    return baseURL
  }

  return { baseURL, getBaseURL }
})

/* =========================
   User Store
========================= */
export const useUserStore = defineStore('user', () => {
  const isRegistered = ref(false)
  const user = ref(null)
  const openChat = ref(null);
  async function registerUser(userName, userClass) {
    const url = BASE_URL + '/api/user/registerUser'

    const body = {
      name: userName,
      school_class: userClass,
      session_key: localStroage.getItem('key'),
    }

    const config = {
      method: 'POST',
      credentials: CREDENTIALS,
      headers: JSON_HEADERS,
      body: JSON.stringify(body)
    }

    const response = await fetch(url, config)
    const data = await response.json()

    user.value = data
    isRegistered.value = !!localStorage.getItem('key')
  }

  async function getUserIsRegistered(session_key=localStorage.getItem('key')) {
    const REGISTERED_URL = BASE_URL + '/api/user/getIsUserRegistered';
    const registration_body = {
      session_key: session_key,
    }
    const registration_configuration = {
      method: 'POST',
      credentials: CREDENTIALS,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registration_body)
    }
  
    const registration_response = await fetch(REGISTERED_URL, registration_configuration);
    const registration_result = await registration_response.json();
    if (registration_result.result == "t" || registration_result == "t") {
      return true;
    } else {
      return null;
    }
  }
  async function getUserDetails(session_key=localStorage.getItem('key')) {
    const DETAILS_URL = BASE_URL + '/api/user/getUserDetails';
    const detailsBody = {
      session_key: session_key
    }
    const detailsConfig = {
      method: 'POST',
      headers: { 
        ...JSON_HEADERS,
        Authorization: `Bearer ${localStorage.getItem('key')}`,
      },
      credentials: CREDENTIALS,
      Authorization: `Bearer ${localStorage.getItem('key')}`,
      body: JSON.stringify(detailsBody),
    }
    const detailsResponse = await fetch(DETAILS_URL, detailsConfig);
    const detailsResult = await detailsResponse.json();
    return detailsResult;
  }

  return { isRegistered, user, registerUser, getUserIsRegistered, getUserDetails }
})

/* =========================
   API Store
========================= */
export const useApiStore = defineStore('api', () => {
  const sessionKey = ref(localStorage.getItem('key'))

  function setSessionKey(key) {
    sessionKey.value = key
    localStorage.setItem('key', key)
  }

async function apiFetch(route, method = 'GET', body = null) {
  const url = BASE_URL + route

  const config = {
    method,
    credentials: 'include',
    headers: { 
      'Content-Type': 'application/json',
      Authorization: `Bearer ${sessionKey.value}`
    }
  }

  if (body) {
    config.body = JSON.stringify({
      ...body,
      session_key: sessionKey.value
    })
  }

  const response = await fetch(url, config)
  const data = await response.json()

  if (!response.ok || data.error) {
    localStorage.setItem('isErrorPresent', true);
    localStorage.setItem('errorMsg', data.error || 'API error')
  }

  if (data.session_key) {
    setSessionKey(data.session_key)
  }

  return data
}


  return {
    sessionKey,
    setSessionKey,
    apiFetch
  }
})
