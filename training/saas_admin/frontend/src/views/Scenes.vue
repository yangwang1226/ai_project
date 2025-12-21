<template>
  <div class="scenes">
    <div class="header">
      <h2>场景管理</h2>
      <el-button type="primary" @click="showDialog(null)" v-if="authStore.isBoss">
        <el-icon><Plus /></el-icon>
        新建场景
      </el-button>
    </div>
    
    <el-card style="margin-top: 20px">
      <el-table :data="scenes" v-loading="loading">
        <el-table-column prop="name" label="场景名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="Prompt模板" width="200">
          <template #default="{ row }">
            <el-text line-clamp="2" style="width: 180px">
              {{ row.prompt_template }}
            </el-text>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" v-if="authStore.isBoss">
          <template #default="{ row }">
            <el-button text type="primary" @click="showDialog(row)">
              编辑
            </el-button>
            <el-button text type="danger" @click="handleDelete(row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingScene ? '编辑场景' : '新建场景'"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="场景名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入场景名称" />
        </el-form-item>
        
        <el-form-item label="场景描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入场景描述"
          />
        </el-form-item>
        
        <el-form-item label="Prompt模板" prop="prompt_template">
          <el-input
            v-model="form.prompt_template"
            type="textarea"
            :rows="5"
            placeholder="例如：你是一个{role}，请帮我{task}"
          />
          <div style="margin-top: 5px; font-size: 12px; color: #909399">
            提示：使用 {变量名} 来定义变量
          </div>
        </el-form-item>
        
        <el-form-item label="变量定义" prop="variables">
          <el-input
            v-model="form.variables"
            type="textarea"
            :rows="3"
            placeholder='JSON格式，例如：{"role": "客服", "task": "解答问题"}'
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import api from '@/utils/request'

const authStore = useAuthStore()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const editingScene = ref(null)
const formRef = ref(null)
const scenes = ref([])

const form = reactive({
  name: '',
  description: '',
  prompt_template: '',
  variables: ''
})

const rules = {
  name: [{ required: true, message: '请输入场景名称', trigger: 'blur' }],
  prompt_template: [{ required: true, message: '请输入Prompt模板', trigger: 'blur' }]
}

const fetchScenes = async () => {
  loading.value = true
  try {
    const data = await api.get('/scenes')
    scenes.value = data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const showDialog = (scene) => {
  editingScene.value = scene
  if (scene) {
    Object.assign(form, scene)
  } else {
    Object.keys(form).forEach(key => form[key] = '')
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (editingScene.value) {
          await api.put(`/scenes/${editingScene.value.id}`, form)
          ElMessage.success('更新成功')
        } else {
          await api.post('/scenes', form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchScenes()
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定要删除这个场景吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  
  try {
    await api.delete(`/scenes/${id}`)
    ElMessage.success('删除成功')
    fetchScenes()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchScenes()
})
</script>

<style scoped>
.scenes .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

