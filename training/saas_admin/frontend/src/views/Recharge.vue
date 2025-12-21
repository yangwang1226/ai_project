<template>
  <div class="recharge">
    <h2>充值</h2>
    
    <el-card style="margin-top: 20px">
      <h3>发起充值</h3>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" style="max-width: 500px; margin-top: 20px">
        <el-form-item label="充值分钟数" prop="minutes">
          <el-input-number v-model="form.minutes" :min="1" :step="100" />
        </el-form-item>
        
        <el-form-item label="充值金额" prop="amount">
          <el-input-number v-model="form.amount" :min="0.01" :step="10" :precision="2" />
          <span style="margin-left: 10px; color: #909399">元</span>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            提交充值申请
          </el-button>
        </el-form-item>
      </el-form>
      
      <el-alert
        title="充值说明"
        type="info"
        :closable="false"
        style="margin-top: 20px"
      >
        <div>1. 提交充值申请后，请联系客服进行充值</div>
        <div>2. 充值完成后，客服会在后台确认，余额将自动到账</div>
        <div>3. 如有疑问，请点击右下角客服图标联系我们</div>
      </el-alert>
    </el-card>
    
    <el-card style="margin-top: 20px">
      <div class="payment-qrcode">
        <h3>联系客服充值</h3>
        <p>请扫描下方二维码添加客服微信</p>
        <div class="qrcode-placeholder">
          <el-icon size="100"><ChatDotRound /></el-icon>
          <div>客服微信二维码</div>
          <div style="font-size: 12px; color: #909399; margin-top: 10px">
            (此处应放置实际的微信二维码图片)
          </div>
        </div>
      </div>
    </el-card>
    
    <el-card style="margin-top: 20px">
      <h3>充值记录</h3>
      <el-table :data="records" v-loading="loading" style="margin-top: 20px">
        <el-table-column prop="minutes" label="充值分钟数" width="120" />
        <el-table-column prop="amount" label="金额（元）" width="120">
          <template #default="{ row }">
            ¥{{ row.amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : 'warning'">
              {{ row.status === 'completed' ? '已完成' : '待确认' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="申请时间" width="180" />
        <el-table-column prop="confirmed_at" label="确认时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/request'

const loading = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const records = ref([])

const form = reactive({
  minutes: 100,
  amount: 10
})

const rules = {
  minutes: [{ required: true, message: '请输入充值分钟数', trigger: 'blur' }],
  amount: [{ required: true, message: '请输入充值金额', trigger: 'blur' }]
}

const fetchRecords = async () => {
  loading.value = true
  try {
    const data = await api.get('/recharge')
    records.value = data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await api.post('/recharge', form)
        ElMessage.success('充值申请已提交，请联系客服')
        fetchRecords()
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.recharge h2 {
  margin-bottom: 20px;
}

.payment-qrcode {
  text-align: center;
  padding: 20px;
}

.qrcode-placeholder {
  margin-top: 20px;
  padding: 40px;
  border: 2px dashed #dcdfe6;
  border-radius: 4px;
  background: #fafafa;
  display: inline-block;
}
</style>

