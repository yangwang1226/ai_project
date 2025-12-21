import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/request'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const isBoss = computed(() => user.value?.role === 'boss')

  async function login(phone, verificationCode) {
    const response = await api.post('/auth/login', {
      phone,
      verification_code: verificationCode
    })
    
    token.value = response.access_token
    localStorage.setItem('token', response.access_token)
    
    await fetchUser()
  }

  async function register(phone, verificationCode, nickname, inviteCode) {
    const response = await api.post('/auth/register', {
      phone,
      verification_code: verificationCode,
      nickname,
      invite_code: inviteCode
    })
    
    token.value = response.access_token
    localStorage.setItem('token', response.access_token)
    
    await fetchUser()
  }

  async function fetchUser() {
    const response = await api.get('/auth/me')
    user.value = response
    localStorage.setItem('user', JSON.stringify(response))
  }

  async function sendVerificationCode(phone) {
    return await api.post('/auth/send-code', { phone })
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    user,
    isAuthenticated,
    isBoss,
    login,
    register,
    fetchUser,
    sendVerificationCode,
    logout
  }
})

