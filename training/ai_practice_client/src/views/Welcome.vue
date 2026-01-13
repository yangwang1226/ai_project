<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <div class="logo-section">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" class="logo-icon">
          <path d="M24 6L42 18V30L24 42L6 30V18L24 6Z" fill="url(#gradient)" />
          <defs>
            <linearGradient id="gradient" x1="6" y1="6" x2="42" y2="42">
              <stop offset="0%" stop-color="#667eea" />
              <stop offset="100%" stop-color="#764ba2" />
            </linearGradient>
          </defs>
        </svg>
        <h1 class="logo-title">AI陪练</h1>
      </div>

      <div v-if="!userName" class="name-input-section">
        <h2 class="welcome-title">欢迎使用AI陪练系统</h2>
        <p class="welcome-subtitle">请告诉我们您的名字，让我们开始吧</p>
        
        <div class="input-group">
          <input
            v-model="inputName"
            type="text"
            placeholder="请输入您的名字"
            class="name-input"
            @keyup.enter="submitName"
            autofocus
          />
          <button 
            class="submit-btn" 
            @click="submitName"
            :disabled="!inputName.trim()"
          >
            继续
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" />
            </svg>
          </button>
        </div>
      </div>

      <div v-else class="loading-section">
        <div class="spinner"></div>
        <p class="loading-text">正在为您准备个性化体验...</p>
      </div>
    </div>

    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const inputName = ref('')
const userName = ref('')

const submitName = () => {
  if (inputName.value.trim()) {
    userName.value = inputName.value.trim()
    // 保存用户名到本地存储
    localStorage.setItem('userName', userName.value)
    // 延迟跳转到引导页
    setTimeout(() => {
      router.push('/onboarding')
    }, 1500)
  }
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.welcome-content {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 48px;
  max-width: 600px;
  width: 100%;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 48px;
  animation: fadeInDown 0.8s ease-out;
}

.logo-icon {
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.2));
  animation: float 3s ease-in-out infinite;
}

.logo-title {
  font-size: 36px;
  font-weight: 700;
  color: white;
  letter-spacing: 2px;
}

.name-input-section {
  animation: fadeIn 1s ease-out 0.3s both;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin-bottom: 16px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.welcome-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
}

.input-group {
  display: flex;
  gap: 12px;
  max-width: 500px;
  margin: 0 auto;
}

.name-input {
  flex: 1;
  padding: 18px 24px;
  font-size: 18px;
  border: none;
  border-radius: 16px;
  background: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  outline: none;
  transition: all 0.3s;
}

.name-input:focus {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
  transform: translateY(-2px);
}

.name-input::placeholder {
  color: #94a3b8;
}

.submit-btn {
  padding: 18px 32px;
  font-size: 18px;
  font-weight: 600;
  color: #667eea;
  background: white;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-section {
  animation: fadeIn 0.5s ease-out;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  margin: 0 auto 24px;
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: 18px;
  color: white;
  font-weight: 500;
}

.background-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  right: -50px;
  animation-delay: 2s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  right: 10%;
  animation-delay: 4s;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .welcome-content {
    padding: 24px;
  }

  .logo-title {
    font-size: 28px;
  }

  .welcome-title {
    font-size: 24px;
  }

  .welcome-subtitle {
    font-size: 16px;
  }

  .input-group {
    flex-direction: column;
  }

  .submit-btn {
    justify-content: center;
  }
}
</style>

