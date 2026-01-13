<template>
  <div class="demo-nav-page">
    <div class="demo-container">
      <div class="demo-header">
        <h1>🎨 AI陪练 - Yoodli风格页面展示</h1>
        <p class="subtitle">点击下方卡片查看不同的页面效果</p>
      </div>

      <div class="pages-grid">
        <div 
          v-for="page in pages" 
          :key="page.path"
          class="page-card"
          @click="navigateTo(page.path)"
        >
          <div class="page-icon">{{ page.icon }}</div>
          <h3 class="page-title">{{ page.title }}</h3>
          <p class="page-description">{{ page.description }}</p>
          <div class="page-badge">{{ page.badge }}</div>
        </div>
      </div>

      <div class="demo-footer">
        <p>✨ 所有页面均采用现代化设计，响应式布局，支持移动端访问</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const pages = [
  {
    path: '/',
    icon: '🏠',
    title: '首页',
    description: '展示产品特性和功能介绍的主页面',
    badge: 'Home'
  },
  {
    path: '/welcome',
    icon: '👋',
    title: '欢迎页',
    description: '收集用户名称的欢迎引导页面',
    badge: 'New'
  },
  {
    path: '/onboarding',
    icon: '🎯',
    title: '引导页',
    description: 'Yoodli风格的多步骤引导流程',
    badge: 'Yoodli Style'
  },
  {
    path: '/select-scene',
    icon: '🎭',
    title: '场景选择',
    description: '选择练习场景的页面',
    badge: 'Interactive'
  },
  {
    path: '/select-voice',
    icon: '🎤',
    title: '声音选择',
    description: '选择AI声音的页面',
    badge: 'Voice'
  },
  {
    path: '/register',
    icon: '📝',
    title: '注册页',
    description: '用户注册和登录页面',
    badge: 'Auth'
  }
]

const navigateTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.demo-nav-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px;
}

.demo-container {
  max-width: 1200px;
  margin: 0 auto;
}

.demo-header {
  text-align: center;
  margin-bottom: 60px;
  color: white;
}

.demo-header h1 {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  color: white;
  background: none;
  -webkit-text-fill-color: white;
}

.subtitle {
  font-size: 20px;
  opacity: 0.95;
  font-weight: 500;
}

.pages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 60px;
}

.page-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.page-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.page-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.page-card:hover::before {
  transform: scaleX(1);
}

.page-icon {
  font-size: 56px;
  margin-bottom: 20px;
  text-align: center;
  animation: float 3s ease-in-out infinite;
}

.page-card:nth-child(2) .page-icon {
  animation-delay: 0.5s;
}

.page-card:nth-child(3) .page-icon {
  animation-delay: 1s;
}

.page-card:nth-child(4) .page-icon {
  animation-delay: 1.5s;
}

.page-card:nth-child(5) .page-icon {
  animation-delay: 2s;
}

.page-card:nth-child(6) .page-icon {
  animation-delay: 2.5s;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
  text-align: center;
}

.page-description {
  font-size: 16px;
  color: #64748b;
  line-height: 1.6;
  text-align: center;
  margin-bottom: 16px;
}

.page-badge {
  display: inline-block;
  padding: 6px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 auto;
  text-align: center;
}

.demo-footer {
  text-align: center;
  color: white;
  font-size: 18px;
  font-weight: 500;
  opacity: 0.9;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 768px) {
  .demo-header h1 {
    font-size: 32px;
  }

  .subtitle {
    font-size: 16px;
  }

  .pages-grid {
    grid-template-columns: 1fr;
  }
}
</style>

