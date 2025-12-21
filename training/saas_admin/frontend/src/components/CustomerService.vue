<template>
  <div class="customer-service" @click="handleClick">
    <el-tooltip content="联系客服" placement="left">
      <div class="service-button">
        <el-icon size="24"><Service /></el-icon>
      </div>
    </el-tooltip>
    
    <!-- 客服对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="联系客服"
      width="400px"
      :append-to-body="true"
    >
      <div class="service-content">
        <div class="qrcode-section">
          <p>请扫描二维码添加客服微信</p>
          <div class="qrcode-placeholder">
            <el-icon size="80"><ChatDotRound /></el-icon>
            <div>客服微信二维码</div>
          </div>
        </div>
        
        <el-divider>或</el-divider>
        
        <div class="contact-info">
          <p><strong>工作时间：</strong>周一至周五 9:00-18:00</p>
          <p><strong>客服电话：</strong>400-xxx-xxxx（示例）</p>
          <p><strong>客服邮箱：</strong>support@example.com（示例）</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const dialogVisible = ref(false)

const handleClick = () => {
  dialogVisible.value = true
}
</script>

<style scoped>
.customer-service {
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: 1000;
}

.service-button {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.service-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.service-content {
  text-align: center;
}

.qrcode-section {
  padding: 20px;
}

.qrcode-section p {
  margin-bottom: 15px;
  color: #606266;
}

.qrcode-placeholder {
  margin: 20px auto;
  padding: 30px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  background: #fafafa;
  display: inline-block;
  color: #909399;
}

.contact-info {
  padding: 20px;
  text-align: left;
}

.contact-info p {
  margin-bottom: 10px;
  color: #606266;
  line-height: 1.8;
}
</style>

