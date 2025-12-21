<template>
  <div class="dashboard">
    <h2>数据看板</h2>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="6">
        <el-card>
          <div class="stat-card">
            <el-icon class="stat-icon" color="#409eff"><UserFilled /></el-icon>
            <div class="stat-content">
              <div class="stat-label">团队成员</div>
              <div class="stat-value">{{ stats.total_users }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card>
          <div class="stat-card">
            <el-icon class="stat-icon" color="#67c23a"><Wallet /></el-icon>
            <div class="stat-content">
              <div class="stat-label">余额（分钟）</div>
              <div class="stat-value">{{ stats.total_balance.toFixed(2) }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card>
          <div class="stat-card">
            <el-icon class="stat-icon" color="#e6a23c"><Clock /></el-icon>
            <div class="stat-content">
              <div class="stat-label">今日使用（分钟）</div>
              <div class="stat-value">{{ stats.total_usage_today.toFixed(2) }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card>
          <div class="stat-card">
            <el-icon class="stat-icon" color="#f56c6c"><TrendCharts /></el-icon>
            <div class="stat-content">
              <div class="stat-label">预计剩余天数</div>
              <div class="stat-value">
                {{ calculateRemainingDays() }}
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card style="margin-top: 20px">
      <h3>快捷操作</h3>
      <div style="margin-top: 20px">
        <el-button type="primary" @click="router.push('/scenes')">
          <el-icon><List /></el-icon>
          管理场景
        </el-button>
        <el-button type="success" @click="router.push('/recharge')">
          <el-icon><Wallet /></el-icon>
          充值
        </el-button>
        <el-button type="info" @click="router.push('/team')">
          <el-icon><UserFilled /></el-icon>
          查看团队
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/request'

const router = useRouter()

const stats = ref({
  total_users: 0,
  total_tenants: 0,
  total_balance: 0,
  total_usage_today: 0
})

const fetchStats = async () => {
  try {
    const data = await api.get('/dashboard/stats')
    stats.value = data
  } catch (error) {
    console.error(error)
  }
}

const calculateRemainingDays = () => {
  if (stats.value.total_usage_today === 0) return '∞'
  const avgDaily = stats.value.total_usage_today
  const days = (stats.value.total_balance / avgDaily).toFixed(0)
  return days > 365 ? '365+' : days
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard h2 {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 48px;
  margin-right: 20px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
</style>

