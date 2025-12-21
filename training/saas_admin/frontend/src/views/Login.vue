<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="title">登录 SaaS管理系统</h2>
      
      <el-form :model="form" :rules="rules" ref="formRef" label-width="0">
        <el-form-item prop="phone">
          <el-input
            v-model="form.phone"
            placeholder="手机号"
            prefix-icon="Phone"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="code">
          <el-input
            v-model="form.code"
            placeholder="验证码"
            prefix-icon="Message"
            size="large"
          >
            <template #append>
              <el-button
                @click="sendCode"
                :disabled="countdown > 0"
              >
                {{ countdown > 0 ? `${countdown}秒` : '发送验证码' }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            @click="handleLogin"
            :loading="loading"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="footer">
          <router-link to="/register">还没有账号？立即注册</router-link>
          <div class="terms">
            登录即表示同意
            <router-link to="/terms">《用户协议》</router-link>
            和
            <router-link to="/privacy">《隐私政策》</router-link>
          </div>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref(null)
const loading = ref(false)
const countdown = ref(0)

const form = reactive({
  phone: '',
  code: ''
})

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ]
}

const sendCode = async () => {
  if (!form.phone || !/^1[3-9]\d{9}$/.test(form.phone)) {
    ElMessage.error('请输入正确的手机号')
    return
  }
  
  try {
    await authStore.sendVerificationCode(form.phone)
    ElMessage.success('验证码已发送')
    
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    console.error(error)
  }
}

const handleLogin = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await authStore.login(form.phone, form.code)
        ElMessage.success('登录成功')
        router.push('/')
      } catch (error) {
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.footer {
  text-align: center;
  margin-top: 20px;
}

.footer a {
  color: #409eff;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}

.terms {
  margin-top: 10px;
  font-size: 12px;
  color: #666;
}
</style>

