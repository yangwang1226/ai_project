<template>
  <div class="usage">
    <h2>使用记录</h2>
    
    <el-card style="margin-top: 20px">
      <el-table :data="records" v-loading="loading">
        <el-table-column prop="user_id" label="用户ID" width="80" />
        <el-table-column prop="minutes_used" label="使用分钟数" width="120">
          <template #default="{ row }">
            {{ row.minutes_used.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明" />
        <el-table-column prop="created_at" label="使用时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/request'

const loading = ref(false)
const records = ref([])

const fetchRecords = async () => {
  loading.value = true
  try {
    const data = await api.get('/usage')
    records.value = data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.usage h2 {
  margin-bottom: 20px;
}
</style>

