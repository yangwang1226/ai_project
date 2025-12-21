<template>
  <div class="practice-page">
    <!-- 顶部工具栏 -->
    <header class="practice-header">
      <button class="back-btn" @click="handleExit">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round"/>
        </svg>
        退出练习
      </button>
      
      <div class="practice-info">
        <div class="timer">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" stroke-width="2"/>
            <path d="M12 6v6l4 2" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>{{ formattedTime }}</span>
        </div>
        <div class="status-indicator" :class="callStatus">
          <div class="status-dot"></div>
          <span>{{ statusText }}</span>
        </div>
      </div>
      
      <div class="score-display">
        <span class="label">得分</span>
        <span class="score">{{ score }}</span>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <div class="practice-content">
      <!-- 左侧：客户形象区 -->
      <div class="customer-panel">
        <div class="customer-avatar-container">
          <!-- 音频波形动画 -->
          <div class="wave-container" :class="{ active: isSpeaking }">
            <div class="wave wave-1"></div>
            <div class="wave wave-2"></div>
            <div class="wave wave-3"></div>
          </div>
          
          <!-- 客户形象 -->
          <div class="customer-avatar" :class="{ speaking: isSpeaking }">
            <div class="avatar-icon">👨</div>
          </div>
        </div>
        
        <div class="customer-info">
          <h3>客户信息</h3>
          <div class="info-tags">
            <span class="tag">👨 男性</span>
            <span class="tag">😊 适中</span>
            <span class="tag">🏠 房地产</span>
          </div>
        </div>

        <!-- 通话控制 -->
        <div class="call-controls">
          <button 
            class="control-btn" 
            :class="{ active: isMuted }"
            @click="toggleMute"
          >
            <svg v-if="!isMuted" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" stroke-width="2"/>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="1" y1="1" x2="23" y2="23" stroke-width="2" stroke-linecap="round"/>
              <path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>{{ isMuted ? '已静音' : '麦克风' }}</span>
          </button>
          
          <button 
            class="control-btn end-call"
            @click="endCall"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm5 13.5l-1.5 1.5-3.5-3.5-3.5 3.5-1.5-1.5 3.5-3.5-3.5-3.5 1.5-1.5 3.5 3.5 3.5-3.5 1.5 1.5-3.5 3.5 3.5 3.5z"/>
            </svg>
            <span>结束</span>
          </button>
        </div>
      </div>

      <!-- 右侧：对话记录区 -->
      <div class="dialogue-panel">
        <div class="dialogue-header">
          <h3>对话记录</h3>
          <button class="export-btn" @click="exportDialogue">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" stroke-width="2" stroke-linecap="round"/>
            </svg>
            导出
          </button>
        </div>
        
        <div class="dialogue-content" ref="dialogueRef">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message"
            :class="message.role"
          >
            <div class="message-avatar">
              {{ message.role === 'customer' ? '👨' : '👤' }}
            </div>
            <div class="message-content">
              <div class="message-header">
                <span class="message-sender">
                  {{ message.role === 'customer' ? '客户' : '我' }}
                </span>
                <span class="message-time">{{ message.time }}</span>
              </div>
              <div class="message-text">{{ message.text }}</div>
              
              <!-- AI建议 -->
              <div v-if="message.suggestion" class="message-suggestion">
                <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                <span>AI建议：{{ message.suggestion }}</span>
              </div>
            </div>
          </div>
          
          <!-- 输入提示 -->
          <div v-if="isListening" class="listening-indicator">
            <div class="pulse-dot"></div>
            <span>正在聆听...</span>
          </div>
        </div>

        <!-- 快捷回复 -->
        <div class="quick-replies">
          <button
            v-for="reply in quickReplies"
            :key="reply"
            class="quick-reply-btn"
            @click="sendQuickReply(reply)"
          >
            {{ reply }}
          </button>
        </div>
      </div>
    </div>

    <!-- 结束对话弹窗 -->
    <transition name="fade">
      <div v-if="showSummary" class="summary-modal">
        <div class="modal-content card">
          <h2>练习总结</h2>
          
          <div class="summary-stats">
            <div class="stat-item">
              <div class="stat-icon">⏱️</div>
              <div class="stat-info">
                <span class="stat-label">通话时长</span>
                <span class="stat-value">{{ formattedTime }}</span>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon">💬</div>
              <div class="stat-info">
                <span class="stat-label">对话轮次</span>
                <span class="stat-value">{{ messages.length }}</span>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon">⭐</div>
              <div class="stat-info">
                <span class="stat-label">本次得分</span>
                <span class="stat-value highlight">{{ score }}</span>
              </div>
            </div>
          </div>

          <div class="summary-feedback">
            <h3>AI评价</h3>
            <p>{{ aiFeedback }}</p>
          </div>

          <div class="modal-actions">
            <button class="btn btn-secondary" @click="practiceAgain">
              再次练习
            </button>
            <button class="btn btn-primary" @click="backToHome">
              返回首页
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const dialogueRef = ref(null)

// 状态
const callStatus = ref('connected')
const isSpeaking = ref(false)
const isMuted = ref(false)
const isListening = ref(false)
const showSummary = ref(false)
const score = ref(85)
const elapsedTime = ref(0)

const messages = ref([
  {
    role: 'customer',
    text: '你好，我想了解一下你们的房源信息。',
    time: '10:00:00'
  },
  {
    role: 'user',
    text: '您好！很高兴为您服务。请问您对哪个区域的房源比较感兴趣？',
    time: '10:00:15',
    suggestion: '回应及时，态度友好'
  }
])

const quickReplies = [
  '好的，我明白了',
  '请您稍等一下',
  '这个问题很好',
  '让我为您详细介绍'
]

const aiFeedback = '本次练习表现良好！你的回应及时，态度专业。建议在介绍产品时可以更加突出客户需求点，多使用开放性问题引导客户表达。'

// 计算属性
const formattedTime = computed(() => {
  const minutes = Math.floor(elapsedTime.value / 60)
  const seconds = elapsedTime.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

const statusText = computed(() => {
  const statusMap = {
    connected: '通话中',
    ended: '已结束',
    paused: '已暂停'
  }
  return statusMap[callStatus.value] || '未知'
})

// 定时器
let timer = null

// 方法
const toggleMute = () => {
  isMuted.value = !isMuted.value
}

const endCall = () => {
  callStatus.value = 'ended'
  if (timer) clearInterval(timer)
  showSummary.value = true
}

const handleExit = () => {
  if (confirm('确定要退出练习吗？当前进度将不会保存。')) {
    router.push('/')
  }
}

const sendQuickReply = (text) => {
  const now = new Date()
  const time = now.toLocaleTimeString('zh-CN', { hour12: false })
  
  messages.value.push({
    role: 'user',
    text,
    time
  })
  
  scrollToBottom()
  
  // 模拟客户回复
  setTimeout(() => {
    simulateCustomerReply()
  }, 2000)
}

const simulateCustomerReply = () => {
  isSpeaking.value = true
  isListening.value = true
  
  setTimeout(() => {
    const replies = [
      '我对市中心的房子比较感兴趣',
      '价格在什么范围？',
      '可以安排看房吗？',
      '这个户型怎么样？'
    ]
    
    const now = new Date()
    const time = now.toLocaleTimeString('zh-CN', { hour12: false })
    
    messages.value.push({
      role: 'customer',
      text: replies[Math.floor(Math.random() * replies.length)],
      time
    })
    
    isSpeaking.value = false
    isListening.value = false
    scrollToBottom()
  }, 3000)
}

const scrollToBottom = () => {
  nextTick(() => {
    if (dialogueRef.value) {
      dialogueRef.value.scrollTop = dialogueRef.value.scrollHeight
    }
  })
}

const exportDialogue = () => {
  console.log('导出对话记录', messages.value)
  alert('对话记录已导出')
}

const practiceAgain = () => {
  showSummary.value = false
  messages.value = []
  elapsedTime.value = 0
  score.value = 0
  callStatus.value = 'connected'
  startTimer()
}

const backToHome = () => {
  router.push('/')
}

const startTimer = () => {
  timer = setInterval(() => {
    elapsedTime.value++
  }, 1000)
}

// 生命周期
onMounted(() => {
  startTimer()
  scrollToBottom()
  
  // 模拟客户说话
  setTimeout(() => {
    isSpeaking.value = true
    setTimeout(() => {
      isSpeaking.value = false
    }, 2000)
  }, 3000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.practice-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

/* 顶部工具栏 */
.practice-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 40px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition);
}

.back-btn:hover {
  background: var(--bg-card);
  border-color: var(--primary);
}

.back-btn svg {
  width: 20px;
  height: 20px;
}

.practice-info {
  display: flex;
  align-items: center;
  gap: 32px;
}

.timer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.timer .icon {
  width: 20px;
  height: 20px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-card);
  border-radius: 20px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.status-indicator.connected .status-dot {
  background: #10b981;
}

.status-indicator.ended .status-dot {
  background: #ef4444;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 20px;
  background: var(--gradient-primary);
  border-radius: 12px;
}

.score-display .label {
  opacity: 0.9;
}

.score-display .score {
  font-size: 24px;
  font-weight: 700;
}

/* 主内容区 */
.practice-content {
  flex: 1;
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 2px;
  background: var(--border-color);
  overflow: hidden;
}

/* 左侧客户面板 */
.customer-panel {
  background: var(--bg-secondary);
  padding: 40px 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.customer-avatar-container {
  position: relative;
  width: 200px;
  height: 200px;
}

.wave-container {
  position: absolute;
  inset: -30px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s;
}

.wave-container.active {
  opacity: 1;
}

.wave {
  width: 6px;
  background: var(--primary);
  border-radius: 3px;
  animation: wave 1.2s ease-in-out infinite;
}

.wave-1 {
  height: 40px;
  animation-delay: 0s;
}

.wave-2 {
  height: 60px;
  animation-delay: 0.2s;
}

.wave-3 {
  height: 40px;
  animation-delay: 0.4s;
}

@keyframes wave {
  0%, 100% {
    height: 40px;
  }
  50% {
    height: 80px;
  }
}

.customer-avatar {
  width: 100%;
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80px;
  transition: var(--transition);
  box-shadow: var(--shadow-lg);
}

.customer-avatar.speaking {
  box-shadow: 0 0 40px rgba(99, 102, 241, 0.6);
  animation: speaking 0.5s ease-in-out infinite;
}

@keyframes speaking {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.customer-info {
  width: 100%;
  text-align: center;
}

.customer-info h3 {
  margin-bottom: 16px;
}

.info-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.tag {
  padding: 6px 12px;
  background: var(--bg-card);
  border-radius: 20px;
  font-size: 14px;
  border: 1px solid var(--border-color);
}

/* 通话控制 */
.call-controls {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: auto;
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition);
}

.control-btn:hover {
  background: var(--bg-primary);
  border-color: var(--primary);
}

.control-btn.active {
  background: var(--primary);
  border-color: var(--primary);
}

.control-btn svg {
  width: 20px;
  height: 20px;
}

.control-btn.end-call {
  background: #ef4444;
  border-color: #ef4444;
  color: white;
}

.control-btn.end-call:hover {
  background: #dc2626;
}

/* 右侧对话面板 */
.dialogue-panel {
  background: var(--bg-secondary);
  display: flex;
  flex-direction: column;
}

.dialogue-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 30px;
  border-bottom: 1px solid var(--border-color);
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition);
}

.export-btn:hover {
  background: var(--bg-primary);
  border-color: var(--primary);
}

.export-btn .icon {
  width: 16px;
  height: 16px;
}

.dialogue-content {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 消息样式 */
.message {
  display: flex;
  gap: 12px;
  animation: slideIn 0.3s ease;
}

.message-avatar {
  width: 40px;
  height: 40px;
  background: var(--bg-card);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.message.user {
  flex-direction: row-reverse;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.message.user .message-header {
  flex-direction: row-reverse;
}

.message-sender {
  font-weight: 600;
  font-size: 14px;
}

.message-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.message-text {
  padding: 12px 16px;
  background: var(--bg-card);
  border-radius: 12px;
  line-height: 1.5;
}

.message.user .message-text {
  background: var(--primary);
}

.message-suggestion {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  padding: 8px 12px;
  background: rgba(16, 185, 129, 0.1);
  border-left: 3px solid #10b981;
  border-radius: 6px;
  font-size: 13px;
  color: #10b981;
}

.message-suggestion .icon {
  width: 14px;
  height: 14px;
}

.listening-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--bg-card);
  border-radius: 12px;
  align-self: center;
}

.pulse-dot {
  width: 12px;
  height: 12px;
  background: var(--primary);
  border-radius: 50%;
  animation: pulse 1.5s ease-in-out infinite;
}

/* 快捷回复 */
.quick-replies {
  padding: 20px 30px;
  border-top: 1px solid var(--border-color);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.quick-reply-btn {
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: var(--transition);
}

.quick-reply-btn:hover {
  background: var(--primary);
  border-color: var(--primary);
}

/* 总结弹窗 */
.summary-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
}

.modal-content {
  max-width: 600px;
  width: 100%;
  padding: 40px;
}

.modal-content h2 {
  text-align: center;
  margin-bottom: 32px;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-card);
  border-radius: 12px;
}

.stat-icon {
  font-size: 32px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
}

.stat-value.highlight {
  color: var(--primary);
}

.summary-feedback {
  margin-bottom: 32px;
  padding: 24px;
  background: var(--bg-card);
  border-radius: 12px;
  border-left: 4px solid var(--primary);
}

.summary-feedback h3 {
  margin-bottom: 12px;
  color: var(--primary);
}

.summary-feedback p {
  line-height: 1.8;
  color: var(--text-secondary);
}

.modal-actions {
  display: flex;
  gap: 16px;
}

.modal-actions .btn {
  flex: 1;
}

/* 响应式 */
@media (max-width: 1024px) {
  .practice-content {
    grid-template-columns: 1fr;
  }
  
  .customer-panel {
    display: none;
  }
}

@media (max-width: 768px) {
  .practice-header {
    padding: 16px 20px;
    flex-wrap: wrap;
    gap: 16px;
  }
  
  .practice-info {
    flex-direction: column;
    gap: 12px;
    width: 100%;
  }
  
  .summary-stats {
    grid-template-columns: 1fr;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}
</style>

