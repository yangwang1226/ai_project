# WebRTC语音通话集成指南

本指南将帮助你在现有页面中集成语音通话功能。

## 方式一：使用VoiceCallButton组件（推荐）

### 1. 在任何页面中导入并使用按钮组件

```vue
<template>
  <div class="my-page">
    <h1>我的页面</h1>
    
    <!-- 使用语音通话按钮组件 -->
    <VoiceCallButton button-text="开始AI对话" />
  </div>
</template>

<script>
import VoiceCallButton from '@/components/VoiceCallButton.vue';

export default {
  name: 'MyPage',
  components: {
    VoiceCallButton
  }
};
</script>
```

### 2. 自定义按钮文本

```vue
<VoiceCallButton button-text="开始练习" />
<VoiceCallButton button-text="语音咨询" />
<VoiceCallButton button-text="AI助手" />
```

## 方式二：编程式导航

### 在Vue组件中使用

```vue
<template>
  <button @click="goToVoiceCall">开始对话</button>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    
    const goToVoiceCall = () => {
      router.push('/voice-call');
    };
    
    return { goToVoiceCall };
  }
};
</script>
```

### 传递参数（可选）

如果需要传递场景、角色等参数：

```vue
<script>
const goToVoiceCall = () => {
  router.push({
    name: 'VoiceCall',
    query: {
      scene: 'sales',
      role: 'customer',
      voice: 'alloy'
    }
  });
};
</script>
```

然后在 `VoiceCall.vue` 中接收参数：

```vue
<script>
import { useRoute } from 'vue-router';

const route = useRoute();
const scene = route.query.scene;
const role = route.query.role;
const voice = route.query.voice || 'alloy';
</script>
```

## 方式三：直接链接

### 使用router-link

```vue
<template>
  <router-link to="/voice-call" class="call-link">
    开始语音通话
  </router-link>
</template>
```

### 带参数的链接

```vue
<router-link 
  :to="{ 
    name: 'VoiceCall', 
    query: { scene: 'interview', voice: 'nova' } 
  }"
  class="call-link">
  开始面试练习
</router-link>
```

## 完整示例：在Practice.vue中集成

假设你想在练习页面添加语音通话功能：

```vue
<template>
  <div class="practice-page">
    <header>
      <h1>AI销售练习</h1>
    </header>
    
    <main>
      <!-- 场景选择 -->
      <div class="scene-selector">
        <h2>选择练习场景</h2>
        <div class="scene-cards">
          <div class="scene-card" @click="startPractice('product')">
            <h3>产品介绍</h3>
            <p>练习产品特性讲解</p>
          </div>
          <div class="scene-card" @click="startPractice('negotiation')">
            <h3>价格谈判</h3>
            <p>提升谈判技巧</p>
          </div>
        </div>
      </div>
      
      <!-- 快速开始按钮 -->
      <div class="quick-start">
        <VoiceCallButton button-text="快速开始练习" />
      </div>
    </main>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import VoiceCallButton from '@/components/VoiceCallButton.vue';

export default {
  name: 'Practice',
  components: {
    VoiceCallButton
  },
  setup() {
    const router = useRouter();
    
    const startPractice = (scene) => {
      router.push({
        name: 'VoiceCall',
        query: { 
          scene: scene,
          mode: 'practice'
        }
      });
    };
    
    return {
      startPractice
    };
  }
};
</script>

<style scoped>
.practice-page {
  padding: 2rem;
}

.scene-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.scene-card {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s;
}

.scene-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.quick-start {
  margin-top: 3rem;
  text-align: center;
}
</style>
```

## 配置WebSocket服务器地址

在开发环境和生产环境使用不同的地址：

### 1. 编辑配置文件

`src/config/webrtc.config.js`:

```javascript
export const WebRTCConfig = {
  websocket: {
    development: 'ws://localhost:8080/ws/realtime',
    production: 'wss://api.yourdomain.com/ws/realtime',
    url: process.env.NODE_ENV === 'production' 
      ? 'wss://api.yourdomain.com/ws/realtime'
      : 'ws://localhost:8080/ws/realtime'
  }
};
```

### 2. 使用环境变量（可选）

在项目根目录创建 `.env` 文件：

```bash
# .env.development
VITE_WS_URL=ws://localhost:8080/ws/realtime

# .env.production
VITE_WS_URL=wss://api.yourdomain.com/ws/realtime
```

然后在配置文件中使用：

```javascript
export const WebRTCConfig = {
  websocket: {
    url: import.meta.env.VITE_WS_URL || 'ws://localhost:8080/ws/realtime'
  }
};
```

## 自定义语音和参数

### 在导航时传递配置

```javascript
const startCustomCall = () => {
  router.push({
    name: 'VoiceCall',
    query: {
      voice: 'nova',           // 使用不同的语音
      scene: 'customer-service',
      model: 'gpt-4-realtime-preview'
    }
  });
};
```

### 在VoiceCall.vue中接收并使用

```javascript
const route = useRoute();

// 使用查询参数覆盖默认配置
const sessionConfig = {
  model: route.query.model || WebRTCConfig.realtimeAPI.model,
  voice: route.query.voice || WebRTCConfig.realtimeAPI.voice,
  // ... 其他配置
};

wsService.value.send({
  type: 'session.create',
  session: sessionConfig
});
```

## 处理权限请求

### 提前请求麦克风权限

在进入语音通话页面前，可以先请求权限：

```vue
<script>
const checkMicrophonePermission = async () => {
  try {
    const result = await navigator.permissions.query({ name: 'microphone' });
    
    if (result.state === 'denied') {
      alert('请在浏览器设置中允许麦克风访问');
      return false;
    }
    
    return true;
  } catch (error) {
    console.error('检查权限失败:', error);
    return true; // 继续尝试
  }
};

const startVoiceCall = async () => {
  const hasPermission = await checkMicrophonePermission();
  if (hasPermission) {
    router.push('/voice-call');
  }
};
</script>
```

## 监听通话状态（高级）

如果需要在父组件中监听通话状态：

### 使用Vuex或Pinia状态管理

```javascript
// store/voiceCall.js
import { defineStore } from 'pinia';

export const useVoiceCallStore = defineStore('voiceCall', {
  state: () => ({
    isConnected: false,
    isRecording: false,
    callDuration: 0
  }),
  actions: {
    setConnected(status) {
      this.isConnected = status;
    },
    setRecording(status) {
      this.isRecording = status;
    },
    updateDuration(duration) {
      this.callDuration = duration;
    }
  }
});
```

在VoiceCall.vue中更新状态：

```javascript
import { useVoiceCallStore } from '@/store/voiceCall';

const callStore = useVoiceCallStore();

// 更新状态
watch(isConnected, (newVal) => {
  callStore.setConnected(newVal);
});
```

在其他组件中访问状态：

```javascript
import { useVoiceCallStore } from '@/store/voiceCall';

const callStore = useVoiceCallStore();
console.log('通话状态:', callStore.isConnected);
```

## 注意事项

1. **HTTPS要求**：WebRTC在生产环境需要HTTPS，本地开发可以使用localhost
2. **浏览器兼容性**：确保目标浏览器支持WebRTC和WebSocket
3. **权限处理**：优雅地处理用户拒绝麦克风权限的情况
4. **错误处理**：添加适当的错误提示和重试机制
5. **资源清理**：确保在页面卸载时正确清理音频资源

## 浏览器兼容性

| 浏览器 | 版本要求 |
|-------|---------|
| Chrome | 74+ |
| Firefox | 66+ |
| Safari | 12+ |
| Edge | 79+ |

## 测试建议

1. 在不同浏览器中测试
2. 测试麦克风权限被拒绝的情况
3. 测试网络断开和重连
4. 测试长时间通话的稳定性
5. 在移动设备上测试（如需支持）

---

需要帮助？请查看 WEBRTC_README.md 获取更多技术细节。

