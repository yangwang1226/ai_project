<template>
  <div class="select-scene-page">
    <div class="container">
      <!-- 进度条 -->
      <div class="progress-bar">
        <div class="progress-step active">
          <div class="step-dot"></div>
          <span>选择场景</span>
        </div>
        <div class="progress-line"></div>
        <div class="progress-step">
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
        <h1>选择练习场景</h1>
        <p>根据你的行业选择最适合的练习场景</p>
      </div>

      <!-- 场景卡片 -->
      <div class="scenes-grid">
        <div
          v-for="scene in scenes"
          :key="scene.id"
          class="scene-card card"
          :class="{ selected: selectedScene === scene.id }"
          @click="selectScene(scene.id)"
        >
          <div class="scene-icon" v-html="scene.icon"></div>
          <h3>{{ scene.title }}</h3>
          <p>{{ scene.description }}</p>
          
          <div class="scene-features">
            <div v-for="feature in scene.features" :key="feature" class="feature-tag">
              {{ feature }}
            </div>
          </div>
          
          <div class="scene-stats">
            <div class="stat">
              <span class="stat-label">难度</span>
              <div class="difficulty-bar">
                <div 
                  class="difficulty-fill" 
                  :style="{ width: `${scene.difficulty * 20}%` }"
                ></div>
              </div>
            </div>
          </div>
          
          <!-- 选中标记 -->
          <div v-if="selectedScene === scene.id" class="selected-mark">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M5 13l4 4L19 7" stroke-width="3" stroke-linecap="round"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="action-buttons fade-in">
        <button class="btn btn-secondary" @click="goBack">
          上一步
        </button>
        <button
          class="btn btn-primary"
          :disabled="!selectedScene"
          @click="nextStep"
        >
          下一步
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-width="2" stroke-linecap="round"/>
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
const selectedScene = ref(null)

const scenes = [
  {
    id: 'education',
    icon: '🎓',
    title: '教育行业',
    description: '模拟课程咨询、家长沟通等场景',
    features: ['课程推荐', '家长沟通', '价格谈判'],
    difficulty: 3
  },
  {
    id: 'real-estate',
    icon: '🏠',
    title: '房地产',
    description: '模拟房产销售、看房接待等场景',
    features: ['房源推荐', '看房接待', '合同签订'],
    difficulty: 4
  },
  {
    id: 'automobile',
    icon: '🚗',
    title: '汽车行业',
    description: '模拟汽车销售、试驾服务等场景',
    features: ['车型介绍', '试驾邀约', '金融方案'],
    difficulty: 3
  }
]

const selectScene = (sceneId) => {
  selectedScene.value = sceneId
}

const goBack = () => {
  router.back()
}

const nextStep = () => {
  if (selectedScene.value) {
    router.push('/select-voice')
  }
}
</script>

<style scoped>
.select-scene-page {
  min-height: 100vh;
  padding: 60px 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 进度条 */
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

.step-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 3px solid var(--border-color);
  transition: var(--transition);
}

.progress-step.active .step-dot {
  background: var(--gradient-primary);
  border-color: var(--primary);
  box-shadow: var(--shadow-glow);
}

.progress-line {
  width: 80px;
  height: 3px;
  background: var(--border-color);
  margin: 0 20px;
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

/* 场景网格 */
.scenes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.scene-card {
  padding: 40px 30px;
  cursor: pointer;
  position: relative;
  transition: var(--transition);
  border: 2px solid var(--border-color);
}

.scene-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary);
  box-shadow: var(--shadow-xl);
}

.scene-card.selected {
  border-color: var(--primary);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  box-shadow: var(--shadow-glow);
}

.scene-icon {
  font-size: 64px;
  margin-bottom: 20px;
  text-align: center;
}

.scene-card h3 {
  margin-bottom: 12px;
  text-align: center;
}

.scene-card p {
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 24px;
}

.scene-features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
  justify-content: center;
}

.feature-tag {
  padding: 6px 12px;
  background: var(--bg-card);
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.scene-stats {
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.difficulty-bar {
  height: 6px;
  background: var(--bg-card);
  border-radius: 3px;
  overflow: hidden;
}

.difficulty-fill {
  height: 100%;
  background: var(--gradient-primary);
  transition: width 0.3s ease;
}

.selected-mark {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: scaleIn 0.3s ease;
}

.selected-mark svg {
  width: 24px;
  height: 24px;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

/* 底部按钮 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
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
  .select-scene-page {
    padding: 40px 20px;
  }
  
  .progress-bar {
    flex-direction: column;
    gap: 20px;
    margin-bottom: 40px;
  }
  
  .progress-line {
    width: 3px;
    height: 40px;
    margin: 0;
  }
  
  .page-header h1 {
    font-size: 32px;
  }
  
  .scenes-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .btn {
    width: 100%;
  }
}
</style>

