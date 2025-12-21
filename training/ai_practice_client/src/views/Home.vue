<template>
  <div class="home">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container">
        <div class="logo">
          <div class="logo-icon">AI</div>
          <span class="logo-text">智能销售练习</span>
        </div>
        <button class="btn btn-primary" @click="goToRegister">
          开始练习
        </button>
      </div>
    </nav>

    <!-- 英雄区域 -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="fade-in">
            AI驱动的销售技能<br>
            <span class="highlight">实战训练平台</span>
          </h1>
          <p class="hero-description fade-in">
            通过AI模拟真实客户场景，随时随地提升你的销售沟通能力
          </p>
          <div class="hero-actions fade-in">
            <button class="btn btn-primary btn-lg" @click="goToRegister">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 12h14M12 5l7 7-7 7" stroke-width="2" stroke-linecap="round"/>
              </svg>
              立即开始
            </button>
            <button class="btn btn-secondary btn-lg">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="2"/>
                <polygon points="10 8 16 12 10 16" fill="currentColor"/>
              </svg>
              观看演示
            </button>
          </div>
        </div>
        
        <!-- 3D动画展示区 -->
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon">🎯</div>
            <div class="card-text">教育行业</div>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon">🏠</div>
            <div class="card-text">房地产</div>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon">🚗</div>
            <div class="card-text">汽车行业</div>
          </div>
          <div class="center-avatar">
            <div class="avatar-ring"></div>
            <div class="avatar-content">
              <svg viewBox="0 0 100 100" class="avatar-icon">
                <circle cx="50" cy="35" r="15" fill="currentColor"/>
                <path d="M 30 70 Q 50 55 70 70 L 70 80 Q 50 90 30 80 Z" fill="currentColor"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 轮播广告区 -->
    <section class="carousel-section">
      <div class="container">
        <div class="carousel">
          <div 
            class="carousel-track" 
            :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
          >
            <div 
              v-for="(slide, index) in slides" 
              :key="index" 
              class="carousel-slide"
            >
              <div class="slide-content card">
                <div class="slide-icon" v-html="slide.icon"></div>
                <h3>{{ slide.title }}</h3>
                <p>{{ slide.description }}</p>
              </div>
            </div>
          </div>
          
          <!-- 轮播指示器 -->
          <div class="carousel-dots">
            <button 
              v-for="(slide, index) in slides" 
              :key="index"
              :class="['dot', { active: currentSlide === index }]"
              @click="currentSlide = index"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- 特性展示 -->
    <section class="features">
      <div class="container">
        <h2 class="section-title">为什么选择我们</h2>
        <div class="features-grid">
          <div class="feature-card card fade-in">
            <div class="feature-icon">🎭</div>
            <h3>真实场景模拟</h3>
            <p>基于真实行业场景，AI智能生成客户对话</p>
          </div>
          <div class="feature-card card fade-in">
            <div class="feature-icon">🎯</div>
            <h3>个性化训练</h3>
            <p>根据你的水平调整难度，精准提升弱项</p>
  </div>
          <div class="feature-card card fade-in">
            <div class="feature-icon">📊</div>
            <h3>数据分析</h3>
            <p>详细的对话分析和改进建议</p>
          </div>
          <div class="feature-card card fade-in">
            <div class="feature-icon">⚡</div>
            <h3>随时随地</h3>
            <p>不受时间地点限制，想练就练</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA区域 -->
    <section class="cta">
      <div class="container">
        <div class="cta-content">
          <h2>准备好提升你的销售技能了吗？</h2>
          <p>加入数千名销售精英，开始你的AI训练之旅</p>
          <button class="btn btn-primary btn-lg" @click="goToRegister">
            免费开始练习
          </button>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-logo">
            <div class="logo-icon">AI</div>
            <span>智能销售练习平台</span>
          </div>
          <p class="footer-text">© 2024 AI销售练习平台. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentSlide = ref(0)

const slides = [
  {
    icon: '🚀',
    title: '新用户专享',
    description: '注册即送100次免费练习机会'
  },
  {
    icon: '🎓',
    title: '专业培训',
    description: '由资深销售导师设计的训练场景'
  },
  {
    icon: '💎',
    title: '限时优惠',
    description: '升级会员享受更多高级功能'
  }
]

let slideTimer = null

const startAutoSlide = () => {
  slideTimer = setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % slides.length
  }, 4000)
}

const stopAutoSlide = () => {
  if (slideTimer) {
    clearInterval(slideTimer)
  }
}

const goToRegister = () => {
  router.push('/register')
}

onMounted(() => {
  startAutoSlide()
})

onUnmounted(() => {
  stopAutoSlide()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
}

/* 导航栏 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
}

.navbar .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: var(--gradient-primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
}

/* 英雄区域 */
.hero {
  padding: 150px 40px 100px;
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.hero .container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.hero-content h1 {
  margin-bottom: 24px;
  animation-delay: 0.1s;
}

.highlight {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 20px;
  color: var(--text-secondary);
  margin-bottom: 40px;
  animation-delay: 0.2s;
}

.hero-actions {
  display: flex;
  gap: 20px;
  animation-delay: 0.3s;
}

.btn-lg {
  padding: 16px 40px;
  font-size: 18px;
}

.icon {
  width: 20px;
  height: 20px;
}

/* 3D视觉效果 */
.hero-visual {
  position: relative;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-card {
  position: absolute;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: var(--shadow-lg);
  animation: float 3s ease-in-out infinite;
}

.card-1 {
  top: 50px;
  left: 50px;
  animation-delay: 0s;
}

.card-2 {
  top: 200px;
  right: 50px;
  animation-delay: 1s;
}

.card-3 {
  bottom: 80px;
  left: 80px;
  animation-delay: 2s;
}

.card-icon {
  font-size: 32px;
}

.card-text {
  font-weight: 600;
  font-size: 16px;
}

.center-avatar {
  position: relative;
  width: 200px;
  height: 200px;
}

.avatar-ring {
  position: absolute;
  inset: -20px;
  border: 3px solid var(--primary);
  border-radius: 50%;
  animation: rotate 20s linear infinite;
  opacity: 0.3;
}

.avatar-content {
  width: 100%;
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-glow);
}

.avatar-icon {
  width: 80px;
  height: 80px;
  color: white;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 轮播区域 */
.carousel-section {
  padding: 80px 40px;
  background: var(--bg-secondary);
}

.carousel {
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  border-radius: 20px;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-slide {
  min-width: 100%;
  padding: 20px;
}

.slide-content {
  text-align: center;
  padding: 60px 40px;
}

.slide-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.slide-content h3 {
  margin-bottom: 16px;
  color: var(--text-primary);
}

.slide-content p {
  font-size: 18px;
  color: var(--text-secondary);
}

.carousel-dots {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 20px 0;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--text-tertiary);
  border: none;
  cursor: pointer;
  transition: var(--transition);
}

.dot.active {
  background: var(--primary);
  width: 32px;
  border-radius: 6px;
}

/* 特性展示 */
.features {
  padding: 100px 40px;
}

.features .container {
  max-width: 1400px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-card {
  text-align: center;
  padding: 40px 30px;
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-card h3 {
  margin-bottom: 12px;
}

.feature-card p {
  color: var(--text-secondary);
}

/* CTA区域 */
.cta {
  padding: 100px 40px;
  background: var(--gradient-primary);
}

.cta-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.cta h2 {
  margin-bottom: 20px;
}

.cta p {
  font-size: 20px;
  margin-bottom: 40px;
  opacity: 0.9;
}

/* 页脚 */
.footer {
  padding: 40px;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
}

.footer-text {
  color: var(--text-secondary);
}

/* 响应式 */
@media (max-width: 1024px) {
  .hero .container {
    grid-template-columns: 1fr;
    gap: 60px;
  }
  
  .hero-visual {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .navbar .container {
    padding: 16px 20px;
  }
  
  .hero {
    padding: 120px 20px 60px;
  }
  
  .hero-actions {
    flex-direction: column;
  }
  
  .btn-lg {
    width: 100%;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
}
</style>

