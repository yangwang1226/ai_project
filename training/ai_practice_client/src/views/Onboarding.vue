<template>
  <div class="onboarding-container">
    <div class="onboarding-header">
      <div class="logo">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <path d="M16 4L28 12V20L16 28L4 20V12L16 4Z" fill="url(#gradient)" />
          <defs>
            <linearGradient id="gradient" x1="4" y1="4" x2="28" y2="28">
              <stop offset="0%" stop-color="#667eea" />
              <stop offset="100%" stop-color="#764ba2" />
            </linearGradient>
          </defs>
        </svg>
        <span class="logo-text">AI陪练</span>
      </div>
    </div>

    <div class="onboarding-content">
      <transition name="slide-fade" mode="out-in">
        <div :key="currentStep" class="step-container">
          <!-- 步骤 1: 欢迎页 -->
          <div v-if="currentStep === 0" class="step welcome-step">
            <h1 class="title">欢迎来到AI陪练，{{ userName }}!</h1>
            <p class="subtitle">我可以帮您做什么?</p>

            <div class="options-grid">
              <div 
                v-for="option in welcomeOptions" 
                :key="option.id"
                class="option-card"
                @click="selectWelcomeOption(option.id)"
              >
                <div class="option-icon">{{ option.icon }}</div>
                <div class="option-text">{{ option.text }}</div>
              </div>
            </div>

            <button class="skip-btn" @click="handleSkip">
              跳过 →
            </button>
          </div>

          <!-- 步骤 2: 角色选择 -->
          <div v-else-if="currentStep === 1" class="step role-step">
            <h2 class="step-title">使用人工智能买家角色帮您完成销售预订会议并成功推进更多销售交易</h2>

            <div class="role-card">
              <div class="role-header">
                <div class="role-icon">❄️</div>
                <span class="role-tag">冷电话</span>
              </div>

              <div class="role-content">
                <div class="role-info">
                  <div class="role-label">买家角色</div>
                  <div class="role-name">销售总监</div>
                </div>

                <div class="role-goals">
                  <div class="goal-label">目标</div>
                  <div class="goal-list">
                    <div class="goal-item">
                      <span class="goal-icon">✓</span>
                      <span>建立融洽关系</span>
                    </div>
                    <div class="goal-item">
                      <span class="goal-icon">✓</span>
                      <span>识别痛点</span>
                    </div>
                    <div class="goal-item">
                      <span class="goal-icon">✓</span>
                      <span>点击要点</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="role-avatar">
                <img :src="avatarUrl" alt="AI Avatar" />
              </div>
            </div>

            <div class="navigation-dots">
              <span 
                v-for="n in 3" 
                :key="n" 
                :class="['dot', { active: dotIndex === n - 1 }]"
              ></span>
            </div>
          </div>

          <!-- 步骤 3: 问题收集 -->
          <div v-else-if="currentStep === 2" class="step question-step">
            <h2 class="step-title">使用人工智能跟进对意见和论点，做好随时应对的准备</h2>

            <div class="question-card">
              <div class="question-header">
                <img class="question-avatar" :src="avatarUrl" alt="Kevin Hooli" />
                <div class="question-user">
                  <div class="user-name">Kevin Hooli</div>
                  <div class="user-role">销售总监</div>
                </div>
              </div>

              <div class="question-content">
                <p class="question-text">
                  Yoodli产品与竞争对手的解决方案相比有何不同? 你们的其他客户发现哪些应用场景或使用案例最有价值?
                </p>
              </div>

              <div class="sparkle-icon">✨</div>
            </div>

            <div class="navigation-dots">
              <span 
                v-for="n in 3" 
                :key="n" 
                :class="['dot', { active: dotIndex === n - 1 }]"
              ></span>
            </div>
          </div>

          <!-- 步骤 4: 反馈选项 -->
          <div v-else-if="currentStep === 3" class="step feedback-step">
            <h2 class="step-title">使用人工智能反馈，精炼您的演讲并产生强烈影响</h2>

            <div class="feedback-options">
              <div class="feedback-card positive">
                <div class="feedback-icon">👍</div>
                <div class="feedback-label">买力</div>
                <p class="feedback-text">很棒的开场白！开始交谈后再谈正事！</p>
              </div>

              <div class="feedback-card growth">
                <div class="feedback-icon">🚩</div>
                <div class="feedback-label">成长区</div>
                <p class="feedback-text">下次，提及您产品的独特卖点，以说明它如何能够提供比竞争对手更多的额外优势。</p>
              </div>
            </div>

            <div class="navigation-dots">
              <span 
                v-for="n in 3" 
                :key="n" 
                :class="['dot', { active: dotIndex === n - 1 }]"
              ></span>
            </div>
          </div>
        </div>
      </transition>

      <div class="navigation-buttons" v-if="currentStep > 0">
        <button class="nav-btn prev-btn" @click="prevStep" :disabled="currentStep === 1">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" />
          </svg>
        </button>
        
        <button class="nav-btn next-btn" @click="nextStep">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentStep = ref(0)
const dotIndex = ref(0)
const userName = ref('朋友')

onMounted(() => {
  // 从localStorage读取用户名
  const savedName = localStorage.getItem('userName')
  if (savedName) {
    userName.value = savedName
  }
})

const avatarUrl = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%23E0E7FF"/%3E%3Ccircle cx="50" cy="40" r="20" fill="%236366F1"/%3E%3Cellipse cx="50" cy="75" rx="30" ry="25" fill="%236366F1"/%3E%3C/svg%3E'

const welcomeOptions = [
  { id: 1, icon: '💎', text: '我正在寻求更多地达成销售协议' },
  { id: 2, icon: '🎭', text: '即将进行的演讲或陈述' },
  { id: 3, icon: '💼', text: '面试准备' },
  { id: 4, icon: '📋', text: '我是沟通教练' }
]

const selectWelcomeOption = (optionId) => {
  console.log('Selected option:', optionId)
  nextStep()
}

const nextStep = () => {
  if (currentStep.value === 0) {
    currentStep.value = 1
    dotIndex.value = 0
  } else if (currentStep.value < 3) {
    currentStep.value++
    dotIndex.value++
  } else {
    // 完成引导，跳转到场景选择页
    router.push('/select-scene')
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    dotIndex.value--
  }
}

const handleSkip = () => {
  router.push('/select-scene')
}
</script>

<style scoped>
.onboarding-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #EFF6FF 0%, #DBEAFE 50%, #BFDBFE 100%);
  display: flex;
  flex-direction: column;
}

.onboarding-header {
  padding: 24px 48px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.onboarding-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  position: relative;
}

.step-container {
  width: 100%;
  max-width: 900px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* 欢迎步骤 */
.welcome-step .title {
  font-size: 42px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-step .subtitle {
  font-size: 24px;
  color: #64748b;
  margin-bottom: 64px;
  font-weight: 500;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  width: 100%;
  margin-bottom: 48px;
}

.option-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 20px;
  padding: 32px 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.option-card:hover {
  transform: translateY(-8px);
  border-color: #6366f1;
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
}

.option-icon {
  font-size: 48px;
  line-height: 1;
}

.option-text {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.4;
}

.skip-btn {
  background: transparent;
  border: none;
  color: #6366f1;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  padding: 12px 24px;
  transition: all 0.3s;
}

.skip-btn:hover {
  color: #4f46e5;
  transform: translateX(4px);
}

/* 角色步骤 */
.role-step .step-title,
.question-step .step-title,
.feedback-step .step-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 48px;
  line-height: 1.4;
  max-width: 800px;
}

.role-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 600px;
  position: relative;
  margin-bottom: 48px;
}

.role-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 32px;
}

.role-icon {
  font-size: 32px;
}

.role-tag {
  background: #EFF6FF;
  color: #2563eb;
  padding: 8px 16px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
}

.role-content {
  text-align: left;
}

.role-label {
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-name {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 24px;
}

.role-goals {
  margin-top: 24px;
}

.goal-label {
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.goal-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  color: #1e293b;
}

.goal-icon {
  width: 24px;
  height: 24px;
  background: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.role-avatar {
  position: absolute;
  top: 40px;
  right: 40px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.role-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 问题步骤 */
.question-card {
  background: #F8FAFC;
  border: 2px solid #e2e8f0;
  border-radius: 24px;
  padding: 32px;
  width: 100%;
  max-width: 600px;
  margin-bottom: 48px;
  position: relative;
  text-align: left;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.question-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question-user {
  flex: 1;
}

.user-name {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.user-role {
  font-size: 14px;
  color: #64748b;
}

.question-content {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.question-text {
  font-size: 16px;
  line-height: 1.6;
  color: #1e293b;
  margin: 0;
}

.sparkle-icon {
  position: absolute;
  top: -10px;
  right: 20px;
  font-size: 32px;
  animation: sparkle 2s ease-in-out infinite;
}

@keyframes sparkle {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
  50% {
    transform: scale(1.2) rotate(180deg);
    opacity: 0.8;
  }
}

/* 反馈步骤 */
.feedback-options {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  max-width: 600px;
  margin-bottom: 48px;
}

.feedback-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-align: left;
  border: 3px solid transparent;
  transition: all 0.3s;
}

.feedback-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.feedback-card.positive {
  border-color: #10b981;
}

.feedback-card.growth {
  border-color: #f59e0b;
}

.feedback-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.feedback-label {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.feedback-card.positive .feedback-label {
  color: #10b981;
}

.feedback-card.growth .feedback-label {
  color: #f59e0b;
}

.feedback-text {
  font-size: 16px;
  line-height: 1.6;
  color: #475569;
  margin: 0;
}

/* 导航点 */
.navigation-dots {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 24px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #cbd5e1;
  transition: all 0.3s;
  cursor: pointer;
}

.dot.active {
  width: 32px;
  border-radius: 6px;
  background: #6366f1;
}

/* 导航按钮 */
.navigation-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

.nav-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #6366f1;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.nav-btn:hover:not(:disabled) {
  background: #4f46e5;
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.nav-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  box-shadow: none;
}

/* 动画 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 响应式 */
@media (max-width: 768px) {
  .onboarding-header {
    padding: 16px 24px;
  }

  .welcome-step .title {
    font-size: 32px;
  }

  .welcome-step .subtitle {
    font-size: 18px;
  }

  .options-grid {
    grid-template-columns: 1fr;
  }

  .step-title {
    font-size: 22px !important;
  }

  .role-card,
  .question-card,
  .feedback-options {
    padding: 24px;
  }

  .role-avatar {
    width: 80px;
    height: 80px;
    top: 24px;
    right: 24px;
  }

  .navigation-buttons {
    position: fixed;
    bottom: 24px;
    left: 0;
    right: 0;
    padding: 0 24px;
  }
}
</style>

