# WebRTC实时语音通话框架使用说明

## 📋 目录

- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [文件结构](#文件结构)
- [核心模块说明](#核心模块说明)
- [配置说明](#配置说明)
- [API文档](#api文档)
- [常见问题](#常见问题)

## 🌟 功能特性

### 已实现功能

- ✅ **实时音频捕获**：使用WebRTC API捕获麦克风音频
- ✅ **音频处理**：支持回声消除、噪音抑制、自动增益控制
- ✅ **WebSocket长连接**：与后端服务建立稳定的双向通信
- ✅ **音频编码传输**：支持Opus/WebM等格式的音频编码和传输
- ✅ **实时音量监测**：可视化显示当前音量级别
- ✅ **自动重连机制**：网络断开时自动尝试重新连接
- ✅ **心跳检测**：维持WebSocket连接活跃状态
- ✅ **音频播放**：播放从服务器接收的音频响应
- ✅ **对话转录**：实时显示对话文本内容
- ✅ **美观的UI界面**：现代化的渐变设计和流畅动画

### 待后端实现功能

- ⏳ 后端WebSocket服务器
- ⏳ 后端与OpenAI Realtime API的集成
- ⏳ 会话管理和状态维护
- ⏳ 音频格式转换（如需要）

## 🏗️ 技术架构

```
┌─────────────┐          ┌──────────────┐          ┌─────────────┐
│   浏览器     │          │   后端服务    │          │  Realtime   │
│  (前端Vue)  │          │  (WebSocket) │          │     API     │
└─────────────┘          └──────────────┘          └─────────────┘
      │                         │                          │
      │  1. WebSocket连接       │                          │
      ├────────────────────────>│                          │
      │                         │                          │
      │  2. 初始化会话          │   建立Realtime会话        │
      ├────────────────────────>├─────────────────────────>│
      │                         │                          │
      │  3. 发送音频流          │   转发音频流              │
      ├────────────────────────>├─────────────────────────>│
      │                         │                          │
      │  4. 接收AI响应          │   接收AI音频/文本         │
      │<────────────────────────┤<─────────────────────────┤
      │                         │                          │
```

### 通信协议

前端与后端使用WebSocket进行通信，消息格式为JSON：

```json
// 创建会话
{
  "type": "session.create",
  "session": {
    "model": "gpt-4-realtime-preview",
    "modalities": ["audio", "text"],
    "voice": "alloy",
    "input_audio_format": "webm",
    "output_audio_format": "pcm16"
  }
}

// 发送音频数据
{
  "type": "input_audio_buffer.append",
  "audio": "base64_encoded_audio_data"
}

// 提交音频（结束输入）
{
  "type": "input_audio_buffer.commit"
}

// 请求生成响应
{
  "type": "response.create"
}
```

## 🚀 快速开始

### 1. 安装依赖

项目已包含在Vue项目中，无需额外安装依赖。

### 2. 配置WebSocket地址

编辑 `src/config/webrtc.config.js`：

```javascript
export const WebRTCConfig = {
  websocket: {
    url: 'ws://localhost:8080/ws/realtime', // 修改为你的后端地址
  }
};
```

或在 `VoiceCall.vue` 中直接修改：

```javascript
const WS_URL = 'ws://localhost:8080/ws/realtime';
```

### 3. 在路由中使用

语音通话页面已添加到路由中，路径为 `/voice-call`。

### 4. 从其他页面导航

在任何Vue组件中导航到语音通话页面：

```vue
<template>
  <button @click="startCall">开始语音通话</button>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    
    const startCall = () => {
      router.push('/voice-call');
    };
    
    return { startCall };
  }
};
</script>
```

### 5. 运行项目

```bash
npm run dev
```

然后访问 `http://localhost:5173/voice-call`

## 📁 文件结构

```
ai_practice_client/
├── src/
│   ├── services/
│   │   ├── webrtc.js          # WebRTC音频服务
│   │   └── websocket.js       # WebSocket连接服务
│   ├── views/
│   │   └── VoiceCall.vue      # 语音通话页面组件
│   ├── config/
│   │   └── webrtc.config.js   # WebRTC配置文件
│   └── router/
│       └── index.js           # 路由配置
└── WEBRTC_README.md           # 使用说明文档
```

## 🔧 核心模块说明

### WebRTCService (webrtc.js)

负责音频的捕获、处理和播放。

**主要方法：**

- `initialize()` - 初始化音频上下文和获取麦克风权限
- `startRecording(callback)` - 开始录音并通过回调发送音频数据
- `stopRecording()` - 停止录音
- `playAudio(audioData, format)` - 播放接收到的音频
- `onVolumeChange(callback)` - 监听音量变化
- `cleanup()` - 清理资源

**使用示例：**

```javascript
import WebRTCService from '@/services/webrtc.js';

const webrtc = new WebRTCService();

// 初始化
await webrtc.initialize();

// 开始录音
webrtc.startRecording((audioData) => {
  console.log('音频数据:', audioData);
  // 发送到服务器
});

// 监听音量
webrtc.onVolumeChange((level) => {
  console.log('音量:', level);
});

// 停止录音
webrtc.stopRecording();

// 播放音频
await webrtc.playAudio(base64AudioData, 'base64');
```

### WebSocketService (websocket.js)

负责与后端的WebSocket通信。

**主要方法：**

- `connect(url)` - 连接到WebSocket服务器
- `send(message)` - 发送JSON消息
- `sendBinary(data)` - 发送二进制数据
- `on(type, handler)` - 注册消息处理器
- `off(type)` - 移除消息处理器
- `onConnectionStateChange(listener)` - 监听连接状态变化
- `close()` - 关闭连接

**使用示例：**

```javascript
import WebSocketService from '@/services/websocket.js';

const ws = new WebSocketService();

// 连接
await ws.connect('ws://localhost:8080/ws/realtime');

// 监听连接状态
ws.onConnectionStateChange((state) => {
  console.log('连接状态:', state);
});

// 注册消息处理器
ws.on('response.audio.delta', (message) => {
  console.log('收到音频:', message);
});

// 发送消息
ws.send({
  type: 'input_audio_buffer.append',
  audio: audioData
});

// 关闭连接
ws.close();
```

## ⚙️ 配置说明

### 音频配置

在 `webrtc.config.js` 中配置音频参数：

```javascript
audio: {
  sampleRate: 24000,        // 采样率
  channelCount: 1,          // 通道数（单声道）
  bitRate: 24000,           // 比特率
  constraints: {
    echoCancellation: true,  // 回声消除
    noiseSuppression: true,  // 噪音抑制
    autoGainControl: true    // 自动增益控制
  }
}
```

### WebSocket配置

```javascript
websocket: {
  url: 'ws://localhost:8080/ws/realtime',
  reconnect: {
    maxAttempts: 5,         // 最大重连次数
    delay: 3000             // 重连延迟(ms)
  },
  heartbeat: {
    interval: 30000,        // 心跳间隔(ms)
    timeout: 10000          // 心跳超时(ms)
  }
}
```

### Realtime API配置

```javascript
realtimeAPI: {
  model: 'gpt-4-realtime-preview',
  voice: 'alloy',           // 语音选项
  turnDetection: {
    type: 'server_vad',     // 语音活动检测
    threshold: 0.5,         // 检测阈值
    silenceDurationMs: 500  // 静音时长
  }
}
```

## 📚 API文档

### 消息类型

#### 前端 → 后端

| 消息类型 | 说明 | 参数 |
|---------|------|------|
| `session.create` | 创建会话 | session配置对象 |
| `input_audio_buffer.append` | 追加音频数据 | base64编码的音频 |
| `input_audio_buffer.commit` | 提交音频缓冲 | 无 |
| `response.create` | 请求生成响应 | 无 |
| `ping` | 心跳检测 | 无 |

#### 后端 → 前端

| 消息类型 | 说明 | 数据 |
|---------|------|------|
| `session.created` | 会话已创建 | 会话信息 |
| `response.audio.delta` | 音频增量数据 | PCM音频数据 |
| `response.audio.done` | 音频响应完成 | 无 |
| `conversation.item.created` | 对话项已创建 | 转录文本 |
| `error` | 错误信息 | 错误详情 |
| `pong` | 心跳响应 | 无 |

## ❓ 常见问题

### 1. 无法访问麦克风

**问题：** 浏览器提示"无法访问麦克风"

**解决方案：**
- 确保浏览器已授予麦克风权限
- 在HTTPS环境下运行（本地开发可以使用localhost）
- 检查系统麦克风设置

### 2. WebSocket连接失败

**问题：** 显示"连接错误"

**解决方案：**
- 确认后端WebSocket服务已启动
- 检查WebSocket URL是否正确
- 查看浏览器控制台的详细错误信息
- 检查防火墙和网络设置

### 3. 音频播放失败

**问题：** 无法播放接收到的音频

**解决方案：**
- 检查音频格式是否匹配
- 确认浏览器支持该音频格式
- 查看控制台错误日志

### 4. 音量显示为0

**问题：** 音量指示器没有变化

**解决方案：**
- 确保麦克风已正确连接
- 检查系统音量设置
- 尝试重新初始化WebRTC服务

### 5. 连接频繁断开

**问题：** WebSocket连接不稳定

**解决方案：**
- 检查网络连接质量
- 调整心跳检测间隔
- 增加重连次数和延迟

## 🔍 调试技巧

### 启用调试模式

在 `VoiceCall.vue` 中设置：

```javascript
const showDebug = ref(true);
```

这将在页面底部显示详细的调试信息。

### 查看消息日志

所有WebSocket消息都会在控制台输出，可以通过浏览器开发者工具查看。

### 测试音频设备

```javascript
// 列出所有音频输入设备
navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    devices.forEach(device => {
      if (device.kind === 'audioinput') {
        console.log(device.label, device.deviceId);
      }
    });
  });
```

## 🚀 性能优化建议

1. **音频数据压缩**：使用适当的编码格式和比特率
2. **缓冲优化**：调整音频块的发送频率
3. **资源清理**：及时释放不用的音频资源
4. **连接池管理**：复用WebSocket连接
5. **错误处理**：优雅处理各种异常情况

## 📝 后续扩展建议

- [ ] 支持多人语音通话
- [ ] 添加录音保存功能
- [ ] 支持音频可视化效果
- [ ] 添加语音识别结果的编辑功能
- [ ] 支持不同语言的语音识别
- [ ] 添加音频增强功能
- [ ] 实现屏幕共享功能

## 📄 许可证

本项目仅供学习和研究使用。

---

如有问题或建议，请联系开发团队。

