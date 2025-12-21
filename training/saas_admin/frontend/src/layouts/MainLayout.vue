<template>
  <el-container class="main-layout">
    <el-aside width="200px">
      <div class="logo">
        <h3>SaaS管理系统</h3>
      </div>
      
      <el-menu
        :default-active="$route.path"
        router
        :unique-opened="true"
      >
        <el-menu-item index="/dashboard" v-if="authStore.isBoss">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据看板</span>
        </el-menu-item>
        
        <el-menu-item index="/scenes">
          <el-icon><List /></el-icon>
          <span>场景管理</span>
        </el-menu-item>
        
        <el-menu-item index="/usage">
          <el-icon><Clock /></el-icon>
          <span>使用记录</span>
        </el-menu-item>
        
        <el-menu-item index="/recharge">
          <el-icon><Wallet /></el-icon>
          <span>充值</span>
        </el-menu-item>
        
        <el-menu-item index="/team">
          <el-icon><UserFilled /></el-icon>
          <span>团队管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-content">
          <span class="greeting">你好，{{ authStore.user?.nickname || authStore.user?.phone }}</span>
          <el-dropdown>
            <el-button text>
              <el-icon><User /></el-icon>
              {{ authStore.user?.role === 'boss' ? '老板' : '员工' }}
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/terms')">
                  用户协议
                </el-dropdown-item>
                <el-dropdown-item @click="router.push('/privacy')">
                  隐私政策
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.el-aside {
  background: #304156;
  color: #fff;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2b3a4a;
}

.logo h3 {
  color: #fff;
  font-size: 16px;
}

.el-menu {
  border-right: none;
  background: #304156;
}

:deep(.el-menu-item) {
  color: #bfcbd9;
}

:deep(.el-menu-item:hover),
:deep(.el-menu-item.is-active) {
  background: #263445 !important;
  color: #409eff;
}

.el-header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.greeting {
  font-size: 16px;
  color: #333;
}

.el-main {
  background: #f0f2f5;
  padding: 20px;
}
</style>

