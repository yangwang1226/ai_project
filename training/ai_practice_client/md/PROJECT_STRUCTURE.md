# 项目结构

```
ai_practice_client/
│
├── 📄 index.html                          # 入口HTML文件
├── 📄 package.json                        # 项目依赖配置
├── 📄 vite.config.js                      # Vite构建配置
│
├── 📚 文档文件/
│   ├── README.md                          # 项目主说明
│   ├── WEBRTC_README.md                   # WebRTC功能详细文档 ⭐
│   ├── INTEGRATION_GUIDE.md               # 集成使用指南 ⭐
│   ├── BACKEND_API_SPEC.md                # 后端API接口规范 ⭐
│   ├── WEBRTC_PROJECT_SUMMARY.md          # 项目总结 ⭐
│   └── PROJECT_STRUCTURE.md               # 本文件
│
└── src/
    │
    ├── 📄 main.js                         # 应用入口
    ├── 📄 App.vue                         # 根组件
    ├── 📄 style.css                       # 全局样式
    │
    ├── 🎯 services/                       # 核心服务模块
    │   ├── webrtc.js                      # ⭐ WebRTC音频服务
    │   │   ├── initialize()               #    初始化音频
    │   │   ├── startRecording()           #    开始录音
    │   │   ├── stopRecording()            #    停止录音
    │   │   ├── playAudio()                #    播放音频
    │   │   ├── onVolumeChange()           #    音量监听
    │   │   └── cleanup()                  #    资源清理
    │   │
    │   └── websocket.js                   # ⭐ WebSocket连接服务
    │       ├── connect()                  #    建立连接
    │       ├── send()                     #    发送消息
    │       ├── on()                       #    消息监听
    │       ├── close()                    #    关闭连接
    │       └── 自动重连机制               #    断线重连
    │
    ├── ⚙️ config/                         # 配置文件
    │   └── webrtc.config.js               # ⭐ WebRTC配置
    │       ├── websocket                  #    WebSocket设置
    │       ├── audio                      #    音频参数
    │       ├── realtimeAPI                #    Realtime API设置
    │       └── ui                         #    UI配置
    │
    ├── 📱 views/                          # 页面组件
    │   ├── Home.vue                       # 首页
    │   ├── Register.vue                   # 注册页
    │   ├── SelectScene.vue                # 场景选择
    │   ├── SelectVoice.vue                # 语音选择
    │   ├── Practice.vue                   # 练习页
    │   └── VoiceCall.vue                  # ⭐ 语音通话页面
    │       ├── 音频可视化                  #    音量波纹效果
    │       ├── 连接管理                    #    建立/断开连接
    │       ├── 录音控制                    #    开始/停止说话
    │       ├── 对话转录                    #    实时文本显示
    │       └── 状态监控                    #    通话状态/时长
    │
    ├── 🧩 components/                     # 可复用组件
    │   └── VoiceCallButton.vue            # ⭐ 语音通话按钮
    │       └── 一键跳转到语音通话页面
    │
    └── 🛣️ router/                         # 路由配置
        └── index.js                       # 路由定义
            └── /voice-call               # ⭐ 语音通话路由

```

## 📊 文件说明

### ⭐ 核心新增文件

| 文件 | 行数 | 功能 |
|-----|------|------|
| `services/webrtc.js` | 374 | WebRTC音频捕获、处理、播放 |
| `services/websocket.js` | 301 | WebSocket长连接管理 |
| `views/VoiceCall.vue` | 744 | 语音通话界面组件 |
| `components/VoiceCallButton.vue` | 58 | 可复用启动按钮 |
| `config/webrtc.config.js` | 83 | 配置管理 |

### 📚 文档文件

| 文档 | 内容 |
|-----|------|
| `WEBRTC_README.md` | 功能特性、API文档、FAQ |
| `INTEGRATION_GUIDE.md` | 三种集成方式、完整示例 |
| `BACKEND_API_SPEC.md` | WebSocket协议、后端实现指南 |
| `WEBRTC_PROJECT_SUMMARY.md` | 项目总结、功能清单 |
| `PROJECT_STRUCTURE.md` | 项目结构图（本文件） |

## 🔄 数据流向

```
┌──────────────────────────────────────────────────────────────┐
│                        VoiceCall.vue                          │
│                      (语音通话页面)                            │
│                                                                │
│  ┌────────────────┐              ┌─────────────────┐          │
│  │  UI Components │              │  State Management │         │
│  │  - 按钮        │              │  - isConnected   │          │
│  │  - 音量显示    │              │  - isRecording   │          │
│  │  - 对话记录    │              │  - volumeLevel   │          │
│  └────────────────┘              └─────────────────┘          │
│         │                                 │                    │
│         └─────────────┬───────────────────┘                    │
│                       │                                        │
│         ┌─────────────▼──────────────┐                         │
│         │                            │                         │
│    ┌────▼──────┐            ┌───────▼────┐                    │
│    │  WebRTC   │            │ WebSocket  │                    │
│    │  Service  │            │  Service   │                    │
│    └────┬──────┘            └───────┬────┘                    │
│         │                           │                         │
└─────────┼───────────────────────────┼─────────────────────────┘
          │                           │
          │                           │
    ┌─────▼──────┐            ┌──────▼───────┐
    │  麦克风     │            │  WebSocket   │
    │  (音频输入) │            │   连接       │
    └─────┬──────┘            └──────┬───────┘
          │                           │
          │                           │
          │                           ▼
          │                    ┌─────────────┐
          │                    │   后端服务   │
          │                    │  (待实现)    │
          │                    └──────┬──────┘
          │                           │
          │                           ▼
          │                    ┌─────────────┐
          │                    │   Realtime  │
          │                    │     API     │
          │                    └──────┬──────┘
          │                           │
          └───────────────────────────┘
                音频数据循环
```

## 🎯 快速定位

### 需要修改WebSocket地址？
👉 `src/config/webrtc.config.js` → `websocket.url`

### 需要调整音频参数？
👉 `src/config/webrtc.config.js` → `audio`

### 需要修改UI样式？
👉 `src/views/VoiceCall.vue` → `<style scoped>`

### 需要添加新功能？
👉 `src/services/webrtc.js` 或 `src/services/websocket.js`

### 需要集成到其他页面？
👉 查看 `INTEGRATION_GUIDE.md`

### 需要了解后端接口？
👉 查看 `BACKEND_API_SPEC.md`

## 📦 依赖关系

```
VoiceCall.vue
    ├── 依赖 → webrtc.js (音频处理)
    ├── 依赖 → websocket.js (网络通信)
    └── 依赖 → webrtc.config.js (配置)

VoiceCallButton.vue
    └── 依赖 → vue-router (路由跳转)

webrtc.js
    └── 依赖 → Web APIs
        ├── AudioContext
        ├── MediaRecorder
        ├── MediaStream
        └── getUserMedia

websocket.js
    └── 依赖 → WebSocket API
```

## 🚀 使用流程

1. **用户点击**：在任何页面点击"开始语音通话"按钮
   ↓
2. **路由跳转**：导航到 `/voice-call` 页面
   ↓
3. **初始化服务**：
   - WebRTCService 请求麦克风权限
   - 初始化音频上下文
   ↓
4. **建立连接**：
   - 点击"建立连接"按钮
   - WebSocketService 连接到后端
   - 发送 `session.create` 消息
   ↓
5. **开始对话**：
   - 点击"开始说话"按钮
   - WebRTC 捕获音频
   - 实时发送到后端
   - 接收并播放AI响应
   ↓
6. **结束对话**：
   - 点击"停止说话"或"断开连接"
   - 清理资源
   - 可选择继续或退出

## 🔧 开发工作流

### 本地开发
```bash
# 启动开发服务器
npm run dev

# 访问语音通话页面
http://localhost:5173/voice-call
```

### 测试
1. 打开浏览器控制台查看日志
2. 启用调试模式（`showDebug = true`）
3. 检查WebSocket连接状态
4. 测试麦克风音频捕获

### 部署
1. 构建生产版本：`npm run build`
2. 配置生产环境WebSocket地址
3. 确保HTTPS环境
4. 测试所有功能

## 📝 代码规范

- ✅ 使用Vue 3 Composition API
- ✅ 代码注释完善（中文）
- ✅ 命名清晰规范
- ✅ 错误处理完整
- ✅ 资源自动清理
- ✅ 零Lint错误

## 🎨 UI层次结构

```
VoiceCall.vue
│
├── Header (顶部栏)
│   ├── 返回按钮
│   ├── 标题
│   └── 状态指示器
│
├── Main Content (主内容)
│   │
│   ├── Audio Visualizer (音频可视化)
│   │   ├── Avatar (头像图标)
│   │   ├── Wave Rings (波纹动画)
│   │   └── Volume Indicator (音量条)
│   │
│   ├── Conversation Info (对话信息)
│   │   ├── Info Card (信息卡片)
│   │   │   ├── 通话时长
│   │   │   ├── 连接状态
│   │   │   └── 采样率
│   │   │
│   │   └── Transcript Card (转录卡片)
│   │       └── 对话列表
│   │
│   ├── Controls (控制按钮)
│   │   ├── 连接/断开按钮
│   │   ├── 录音/停止按钮
│   │   └── 静音按钮
│   │
│   └── Debug Panel (调试面板)
│       └── 调试信息显示
│
```

## 🔐 安全考虑

| 方面 | 实现 |
|-----|------|
| 麦克风权限 | ✅ 安全请求和错误处理 |
| 数据传输 | ✅ 支持WSS加密连接 |
| 输入验证 | ✅ 所有输入数据验证 |
| 错误处理 | ✅ 完善的异常捕获 |
| 资源清理 | ✅ 自动释放资源 |

## 📈 性能特性

| 特性 | 说明 |
|-----|------|
| 懒加载 | ✅ 路由级别代码分割 |
| 音频优化 | ✅ Opus编码，24kHz采样 |
| 网络优化 | ✅ WebSocket长连接 |
| UI优化 | ✅ GPU加速动画 |
| 内存管理 | ✅ 及时清理资源 |

---

**提示**: 如需详细信息，请查看对应的文档文件。

