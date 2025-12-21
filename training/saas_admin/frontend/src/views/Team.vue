<template>
  <div class="team">
    <h2>团队管理</h2>
    
    <el-card style="margin-top: 20px" v-if="tenant">
      <h3>团队信息</h3>
      <el-descriptions :column="2" border style="margin-top: 20px">
        <el-descriptions-item label="团队名称">
          {{ tenant.name }}
        </el-descriptions-item>
        <el-descriptions-item label="邀请码">
          <el-tag>{{ tenant.invite_code }}</el-tag>
          <el-button
            text
            type="primary"
            @click="copyInviteCode"
            style="margin-left: 10px"
          >
            复制
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="余额（分钟）">
          {{ tenant.balance_minutes.toFixed(2) }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ tenant.created_at }}
        </el-descriptions-item>
      </el-descriptions>
      
      <el-alert
        title="邀请团队成员"
        type="info"
        :closable="false"
        style="margin-top: 20px"
      >
        分享邀请码 <el-tag>{{ tenant.invite_code }}</el-tag> 给团队成员，让他们在注册时输入即可加入团队
      </el-alert>
    </el-card>
    
    <el-card style="margin-top: 20px" v-else>
      <el-empty description="您还未创建或加入团队">
        <el-button type="primary" @click="showCreateDialog">创建团队</el-button>
      </el-empty>
    </el-card>
    
    <!-- 创建团队对话框 -->
    <el-dialog v-model="dialogVisible" title="创建团队" width="400px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="团队名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入团队名称" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="submitting">
          创建
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/request'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const tenant = ref(null)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({
  name: ''
})

const rules = {
  name: [{ required: true, message: '请输入团队名称', trigger: 'blur' }]
}

const fetchTenant = async () => {
  try {
    const data = await api.get('/tenants/my')
    tenant.value = data
  } catch (error) {
    console.error(error)
  }
}

const showCreateDialog = () => {
  form.name = ''
  dialogVisible.value = true
}

const handleCreate = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await api.post('/tenants', form)
        ElMessage.success('团队创建成功')
        dialogVisible.value = false
        await authStore.fetchUser()
        fetchTenant()
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const copyInviteCode = () => {
  navigator.clipboard.writeText(tenant.value.invite_code)
  ElMessage.success('邀请码已复制')
}

onMounted(() => {
  fetchTenant()
})
</script>

<style scoped>
.team h2 {
  margin-bottom: 20px;
}
</style>

