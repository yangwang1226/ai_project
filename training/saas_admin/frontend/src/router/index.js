import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { requiresBoss: true }
      },
      {
        path: 'scenes',
        name: 'Scenes',
        component: () => import('@/views/Scenes.vue')
      },
      {
        path: 'usage',
        name: 'Usage',
        component: () => import('@/views/Usage.vue')
      },
      {
        path: 'recharge',
        name: 'Recharge',
        component: () => import('@/views/Recharge.vue')
      },
      {
        path: 'team',
        name: 'Team',
        component: () => import('@/views/Team.vue')
      },
      {
        path: 'terms',
        name: 'Terms',
        component: () => import('@/views/Terms.vue')
      },
      {
        path: 'privacy',
        name: 'Privacy',
        component: () => import('@/views/Privacy.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.token) {
    next('/login')
  } else if (to.meta.requiresBoss && authStore.user?.role !== 'boss') {
    ElMessage.error('权限不足，只有老板可以访问')
    next('/scenes')
  } else if ((to.path === '/login' || to.path === '/register') && authStore.token) {
    next('/')
  } else {
    next()
  }
})

export default router

