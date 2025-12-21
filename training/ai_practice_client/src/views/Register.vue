<template>
  <div class="register-page">
    <div class="register-container">
      <!-- 返回按钮 -->
      <button class="back-btn" @click="goBack">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>

      <!-- 左侧装饰 -->
      <div class="register-visual">
        <div class="visual-content">
          <div class="floating-shapes">
            <div class="shape shape-1"></div>
            <div class="shape shape-2"></div>
            <div class="shape shape-3"></div>
          </div>
          <h2>开启你的AI<br>销售训练之旅</h2>
          <p>通过智能对话练习，快速提升你的销售技巧</p>
        </div>
      </div>

      <!-- 注册表单 -->
      <div class="register-form-container">
        <div class="form-header">
          <h1>欢迎加入</h1>
          <p>只需一步，即刻开始练习</p>
        </div>

        <form class="register-form" @submit.prevent="handleRegister">
          <!-- 手机号输入 -->
          <div class="form-group">
            <label for="phone">手机号</label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              class="input"
              placeholder="请输入11位手机号"
              maxlength="11"
              :class="{ error: errors.phone }"
            />
            <span v-if="errors.phone" class="error-text">{{ errors.phone }}</span>
          </div>

          <!-- 验证码输入 -->
          <div class="form-group">
            <label for="code">验证码</label>
            <div class="code-input-group">
              <input
                id="code"
                v-model="form.code"
                type="text"
                class="input"
                placeholder="请输入验证码"
                maxlength="6"
                :class="{ error: errors.code }"
              />
              <button
                type="button"
                class="btn btn-secondary code-btn"
                :disabled="countdown > 0"
                @click="sendCode"
              >
                {{ countdown > 0 ? `${countdown}秒后重试` : '发送验证码' }}
              </button>
            </div>
            <span v-if="errors.code" class="error-text">{{ errors.code }}</span>
          </div>

          <!-- 用户协议 -->
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input v-model="form.agreed" type="checkbox" />
              <span class="checkbox-text">
                我已阅读并同意
                <a href="#" class="link">《用户协议》</a>
                和
                <a href="#" class="link">《隐私政策》</a>
              </span>
            </label>
            <span v-if="errors.agreed" class="error-text">{{ errors.agreed }}</span>
          </div>

          <!-- 提交按钮 -->
          <button
            type="submit"
            class="btn btn-primary submit-btn"
            :disabled="loading"
          >
            <span v-if="!loading">立即注册</span>
            <span v-else class="loading">
              <span class="spinner"></span>
              注册中...
            </span>
          </button>
        </form>

        <!-- 额外信息 -->
        <div class="form-footer">
          <p class="info-text">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            注册即送100次免费练习机会
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const countdown = ref(0)

const form = reactive({
  phone: '',
  code: '',
  agreed: false
})

const errors = reactive({
  phone: '',
  code: '',
  agreed: ''
})

const validateForm = () => {
  errors.phone = ''
  errors.code = ''
  errors.agreed = ''
  
  let isValid = true
  
  if (!form.phone) {
    errors.phone = '请输入手机号'
    isValid = false
  } else if (!/^1[3-9]\d{9}$/.test(form.phone)) {
    errors.phone = '请输入正确的手机号'
    isValid = false
  }
  
  if (!form.code) {
    errors.code = '请输入验证码'
    isValid = false
  } else if (form.code.length !== 6) {
    errors.code = '验证码为6位数字'
    isValid = false
  }
  
  if (!form.agreed) {
    errors.agreed = '请阅读并同意用户协议'
    isValid = false
  }
  
  return isValid
}

const sendCode = () => {
  if (!form.phone) {
    errors.phone = '请先输入手机号'
    return
  }
  
  if (!/^1[3-9]\d{9}$/.test(form.phone)) {
    errors.phone = '请输入正确的手机号'
    return
  }
  
  // 模拟发送验证码
  console.log('发送验证码到:', form.phone)
  
  // 开始倒计时
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const handleRegister = () => {
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  
  // 模拟注册请求
  setTimeout(() => {
    loading.value = false
    console.log('注册成功', form)
    // 跳转到场景选择页
    router.push('/select-scene')
  }, 1500)
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
}

.back-btn {
  position: absolute;
  top: 40px;
  left: 40px;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  z-index: 10;
}

.back-btn:hover {
  background: var(--bg-card);
  border-color: var(--primary);
}

.back-btn svg {
  width: 24px;
  height: 24px;
}

.register-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1200px;
  width: 100%;
  background: var(--bg-secondary);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-color);
}

/* 左侧视觉区域 */
.register-visual {
  background: var(--gradient-primary);
  padding: 80px 60px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.visual-content {
  position: relative;
  z-index: 2;
}

.visual-content h2 {
  font-size: 42px;
  margin-bottom: 20px;
  line-height: 1.2;
}

.visual-content p {
  font-size: 18px;
  opacity: 0.9;
}

.floating-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 200px;
  height: 200px;
  top: -50px;
  right: -50px;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  bottom: 50px;
  left: -30px;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  top: 50%;
  right: 20%;
  animation-delay: 4s;
}

/* 右侧表单区域 */
.register-form-container {
  padding: 80px 60px;
}

.form-header {
  margin-bottom: 40px;
}

.form-header h1 {
  font-size: 36px;
  margin-bottom: 12px;
}

.form-header p {
  color: var(--text-secondary);
  font-size: 16px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: var(--text-primary);
}

.input.error {
  border-color: #ef4444;
}

.error-text {
  color: #ef4444;
  font-size: 14px;
}

.code-input-group {
  display: flex;
  gap: 12px;
}

.code-input-group .input {
  flex: 1;
}

.code-btn {
  white-space: nowrap;
  padding: 14px 24px;
}

.checkbox-group {
  margin-top: 8px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  margin-top: 2px;
  cursor: pointer;
}

.checkbox-text {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.5;
}

.link {
  color: var(--primary-light);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.submit-btn {
  margin-top: 16px;
  width: 100%;
  font-size: 18px;
  padding: 16px;
}

.loading {
  display: flex;
  align-items: center;
  gap: 12px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.form-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.info-text {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
}

.info-text .icon {
  width: 20px;
  height: 20px;
  color: var(--primary-light);
}

/* 响应式 */
@media (max-width: 1024px) {
  .register-container {
    grid-template-columns: 1fr;
  }
  
  .register-visual {
    padding: 60px 40px;
  }
  
  .register-form-container {
    padding: 60px 40px;
  }
}

@media (max-width: 768px) {
  .back-btn {
    top: 20px;
    left: 20px;
  }
  
  .register-visual {
    padding: 40px 30px;
  }
  
  .visual-content h2 {
    font-size: 32px;
  }
  
  .register-form-container {
    padding: 40px 30px;
  }
  
  .form-header h1 {
    font-size: 28px;
  }
  
  .code-input-group {
    flex-direction: column;
  }
  
  .code-btn {
    width: 100%;
  }
}
</style>

