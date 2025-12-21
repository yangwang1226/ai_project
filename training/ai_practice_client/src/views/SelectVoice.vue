<template>
  <div class="select-voice-page">
    <div class="container">
      <!-- 进度条 -->
      <div class="progress-bar">
        <div class="progress-step completed">
          <div class="step-dot">✓</div>
          <span>选择场景</span>
        </div>
        <div class="progress-line completed"></div>
        <div class="progress-step active">
          <div class="step-dot"></div>
          <span>配置客户</span>
        </div>
        <div class="progress-line"></div>
        <div class="progress-step">
          <div class="step-dot"></div>
          <span>开始练习</span>
        </div>
      </div>

      <!-- 页面标题 -->
      <div class="page-header fade-in">
        <h1>配置模拟客户</h1>
        <p>选择客户的性别和性格特征，让练习更加真实</p>
      </div>

      <div class="config-sections">
        <!-- 性别选择 -->
        <section class="config-section fade-in">
          <h2 class="section-title">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2"/>
              <circle cx="12" cy="7" r="4" stroke-width="2"/>
            </svg>
            客户性别
          </h2>
          
          <div class="options-grid">
            <div
              v-for="gender in genders"
              :key="gender.id"
              class="option-card card"
              :class="{ selected: selectedGender === gender.id }"
              @click="selectedGender = gender.id"
            >
              <div class="option-icon">{{ gender.icon }}</div>
              <h3>{{ gender.label }}</h3>
              <p>{{ gender.description }}</p>
              
              <div v-if="selectedGender === gender.id" class="selected-mark">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M5 13l4 4L19 7" stroke-width="3" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
          </div>
        </section>

        <!-- 性格选择 -->
        <section class="config-section fade-in">
          <h2 class="section-title">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke-width="2" stroke-linecap="round"/>
              <line x1="9" y1="9" x2="9.01" y2="9" stroke-width="2" stroke-linecap="round"/>
              <line x1="15" y1="9" x2="15.01" y2="9" stroke-width="2" stroke-linecap="round"/>
            </svg>
            客户性格
          </h2>
          
          <div class="options-grid">
            <div
              v-for="mood in moods"
              :key="mood.id"
              class="option-card card"
              :class="{ selected: selectedMood === mood.id }"
              @click="selectedMood = mood.id"
            >
              <div class="option-icon">{{ mood.icon }}</div>
              <h3>{{ mood.label }}</h3>
              <p>{{ mood.description }}</p>
              
              <div class="mood-indicator">
                <div 
                  class="indicator-bar" 
                  :class="mood.id"
                  :style="{ width: `${mood.intensity}%` }"
                ></div>
              </div>
              
              <div v-if="selectedMood === mood.id" class="selected-mark">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M5 13l4 4L19 7" stroke-width="3" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
          </div>
        </section>

        <!-- 预览区域 -->
        <section class="preview-section card fade-in">
          <h3>客户预览</h3>
          <div class="preview-content">
            <div class="preview-avatar">
              <div class="avatar-ring"></div>
              <div class="avatar-icon">
                {{ selectedGender === 'male' ? '👨' : selectedGender === 'female' ? '👩' : '❓' }}
              </div>
            </div>
            <div class="preview-info">
              <div class="info-row">
                <span class="label">性别：</span>
                <span class="value">
                  {{ genders.find(g => g.id === selectedGender)?.label || '未选择' }}
                </span>
              </div>
              <div class="info-row">
                <span class="label">性格：</span>
                <span class="value">
                  {{ moods.find(m => m.id === selectedMood)?.label || '未选择' }}
                </span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- 底部按钮 -->
      <div class="action-buttons fade-in">
        <button class="btn btn-secondary" @click="goBack">
          上一步
        </button>
        <button
          class="btn btn-primary"
          :disabled="!selectedGender || !selectedMood"
          @click="startPractice"
        >
          开始练习
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" stroke-width="2"/>
            <polygon points="10 8 16 12 10 16" fill="currentColor"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedGender = ref(null)
const selectedMood = ref(null)

const genders = [
  {
    id: 'male',
    icon: '👨',
    label: '男性',
    description: '男性客户声音，沉稳有力'
  },
  {
    id: 'female',
    icon: '👩',
    label: '女性',
    description: '女性客户声音，温和亲切'
  }
]

const moods = [
  {
    id: 'cold',
    icon: '😐',
    label: '冷漠',
    description: '对产品不感兴趣，态度冷淡',
    intensity: 80
  },
  {
    id: 'moderate',
    icon: '😊',
    label: '适中',
    description: '态度中立，需要引导沟通',
    intensity: 50
  },
  {
    id: 'positive',
    icon: '😄',
    label: '积极',
    description: '对产品感兴趣，配合度高',
    intensity: 90
  }
]

const goBack = () => {
  router.back()
}

const startPractice = () => {
  if (selectedGender.value && selectedMood.value) {
    router.push('/practice')
  }
}
</script>

<style scoped>
.select-voice-page {
  min-height: 100vh;
  padding: 60px 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 进度条（复用之前的样式并添加完成状态） */
.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 60px;
  gap: 20px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: var(--text-tertiary);
  transition: var(--transition);
}

.progress-step.active {
  color: var(--primary);
}

.progress-step.completed {
  color: var(--primary-light);
}

.step-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 3px solid var(--border-color);
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.progress-step.active .step-dot {
  background: var(--gradient-primary);
  border-color: var(--primary);
  box-shadow: var(--shadow-glow);
}

.progress-step.completed .step-dot {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.progress-line {
  width: 80px;
  height: 3px;
  background: var(--border-color);
  transition: var(--transition);
}

.progress-line.completed {
  background: var(--primary);
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 60px;
}

.page-header h1 {
  font-size: 42px;
  margin-bottom: 16px;
}

.page-header p {
  font-size: 18px;
  color: var(--text-secondary);
}

/* 配置区域 */
.config-sections {
  display: flex;
  flex-direction: column;
  gap: 50px;
  margin-bottom: 60px;
}

.config-section {
  animation-delay: 0.1s;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
  font-size: 24px;
}

.section-title .icon {
  width: 28px;
  height: 28px;
  color: var(--primary);
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.option-card {
  padding: 32px 24px;
  cursor: pointer;
  position: relative;
  transition: var(--transition);
  border: 2px solid var(--border-color);
  text-align: center;
}

.option-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary-light);
}

.option-card.selected {
  border-color: var(--primary);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.option-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.option-card h3 {
  margin-bottom: 8px;
}

.option-card p {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 16px;
}

.mood-indicator {
  height: 6px;
  background: var(--bg-card);
  border-radius: 3px;
  overflow: hidden;
}

.indicator-bar {
  height: 100%;
  transition: width 0.3s ease;
}

.indicator-bar.cold {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.indicator-bar.moderate {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.indicator-bar.positive {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.selected-mark {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: scaleIn 0.3s ease;
}

.selected-mark svg {
  width: 20px;
  height: 20px;
}

/* 预览区域 */
.preview-section {
  padding: 32px;
  animation-delay: 0.2s;
}

.preview-section h3 {
  margin-bottom: 24px;
  text-align: center;
}

.preview-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
}

.preview-avatar {
  position: relative;
  width: 120px;
  height: 120px;
}

.avatar-ring {
  position: absolute;
  inset: -10px;
  border: 3px solid var(--primary);
  border-radius: 50%;
  animation: rotate 10s linear infinite;
  opacity: 0.3;
}

.avatar-icon {
  width: 100%;
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
}

.preview-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.info-row .label {
  color: var(--text-secondary);
  font-weight: 600;
}

.info-row .value {
  color: var(--text-primary);
  font-size: 18px;
}

/* 底部按钮 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  animation-delay: 0.3s;
}

.action-buttons .btn {
  min-width: 160px;
}

.action-buttons .icon {
  width: 20px;
  height: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .select-voice-page {
    padding: 40px 20px;
  }
  
  .page-header h1 {
    font-size: 32px;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .preview-content {
    flex-direction: column;
    gap: 24px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .btn {
    width: 100%;
  }
}
</style>

