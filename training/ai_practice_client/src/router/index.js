import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/demo',
    name: 'DemoNav',
    component: () => import('@/views/DemoNav.vue')
  },
  {
    path: '/welcome',
    name: 'Welcome',
    component: () => import('@/views/Welcome.vue')
  },
  {
    path: '/onboarding',
    name: 'Onboarding',
    component: () => import('@/views/Onboarding.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/select-scene',
    name: 'SelectScene',
    component: () => import('@/views/SelectScene.vue')
  },
  {
    path: '/select-voice',
    name: 'SelectVoice',
    component: () => import('@/views/SelectVoice.vue')
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('@/views/Practice.vue')
  },
  {
    path: '/voice-call',
    name: 'VoiceCall',
    component: () => import('@/views/VoiceCall.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

