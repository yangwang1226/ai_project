# AI实时语音对话系统 - 完整说明

## 🎯 项目概述

这是一个基于WebRTC和DashScope Realtime API的实时语音对话系统，专为销售培训场景设计。系统包含完整的前后端实现，支持实时语音交互、语音识别、文本转录等功能。

## 📦 系统组成

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     完整系统架构                              │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────────┐         ┌─────────────┐
│  前端客户端   │         │  WebSocket服务器  │         │  DashScope  │
│              │         │                  │         │  Realtime   │
│  Vue 3       │<------->│  Python         │<------->│     API     │
│  WebRTC      │  WS     │  asyncio        │  API    │   (阿里云)  │
│              │         │  dashscope SDK  │         │             │
└──────────────┘         └──────────────────┘         └─────────────┘
     ↓                            ↓                          ↓
  用户界面                    消息转发                   AI处理
  音频捕获                    格式转换                   语音合成
  实时显示                    会话管理                   语音识别
```

### 核心技术栈

#### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **路由**: Vue Router
- **音频**: WebRTC API, AudioContext, ScriptProcessorNode
- **通信**: WebSocket
- **样式**: CSS3 (渐变、动画)

#### 后端
- **语言**: Python 3.8+
- **异步框架**: asyncio
- **WebSocket库**: websockets
- **AI SDK**: dashscope
- **日志**: logging

#### 音频处理
- **采样率**: 24000 Hz
- **格式**: PCM 16-bit
- **通道**: 单声道 (Mono)
- **传输**: Base64编码

## 📂 项目结构

```
ai_project/training/
│
├── 📄 start_backend.bat          # 后端启动脚本
├── 📄 start_frontend.bat         # 前端启动脚本
├── 📄 QUICK_START.md            # 快速启动指南
├── 📄 README_SYSTEM.md          # 本文件
│
├── 🎨 ai_practice_client/       # 前端项目
│   ├── src/
│   │   ├── services/
│   │   │   ├── webrtc.js       # WebRTC音频服务
│   │   │   └── websocket.js    # WebSocket连接服务
│   │   ├── views/
│   │   │   └── VoiceCall.vue   # 语音通话页面
│   │   ├── components/
│   │   │   └── VoiceCallButton.vue  # 启动按钮
│   │   ├── config/
│   │   │   └── webrtc.config.js     # 配置文件
│   │   └── router/
│   │       └── index.js        # 路由配置
│   ├── package.json
│   └── 文档...
│
└── 🐍 llm/realtime/qwen/dashscope/  # 后端项目
    ├── websocket_server.py     # WebSocket服务器
    ├── run_server_vad.py       # 命令行客户端
    ├── prompts/
    │   └── sales_training.txt  # 提示词文件
    ├── requirements.txt        # Python依赖
    ├── B64PCMPlayer.py        # 音频播放器
    └── README_WEBSOCKET.md    # 后端文档
```

## 🔄 数据流详解

### 1. 连接建立流程

```
用户点击"建立连接"
    ↓
前端: 发送 session.create 消息
    ↓
后端: 创建 DashScope 会话
    ↓
后端: 配置语音、VAD等参数
    ↓
后端: 返回 session.created
    ↓
前端: 显示"已连接"状态
```

### 2. 语音输入流程

```
用户点击"开始说话"
    ↓
前端: 启动麦克风录音
    ↓
前端: 每2048样本获取PCM数据
    ↓
前端: 转换为Int16 PCM
    ↓
前端: Base64编码
    ↓
前端: 通过WebSocket发送 input_audio_buffer.append
    ↓
后端: 接收音频数据
    ↓
后端: 转发给DashScope API
    ↓
DashScope: 实时语音识别
    ↓
DashScope: VAD检测用户停止说话
```

### 3. AI响应流程

```
DashScope: 用户停止说话（VAD检测）
    ↓
DashScope: 生成AI响应
    ↓
DashScope: 流式返回音频片段 (response.audio.delta)
    ↓
后端: 转发音频给前端
    ↓
前端: 接收音频Base64数据
    ↓
前端: 解码并播放PCM音频
    ↓
同时: 文本转录 (conversation.item.created)
    ↓
前端: 显示对话内容
```

## 🎭 默认场景：销售培训

### 场景设定

**AI角色**: 咨询培训机构的学生家长
**用户角色**: 新东方销售人员
**目标**: 练习销售沟通技巧

### 场景特点

1. **严格的角色约束**
   - AI只能扮演家长角色
   - 不能介绍课程或产品
   - 违反角色会自我纠正

2. **结构化对话流程**
   - 必须以"家长您好"开头
   - 有预设的问题队列
   - 根据销售话术触发顾虑

3. **智能顾虑触发**
   - 学校分析相关顾虑
   - 成绩诊断相关顾虑
   - 课程介绍相关顾虑

4. **自动评价系统**
   - 流畅度打分（100分制）
   - 认可度评价（不满意/一般/积极）
   - 评价和建议

### 示例对话

```
销售: 家长您好，我是新东方的课程顾问小王，请问有什么可以帮您的？

家长: 您好，我想了解一下新东方这边的培训课程？

销售: 好的，请问孩子现在几年级了？在哪个学校上学呢？

家长: 七年级，在北环学校。

销售: 北环是一所很不错的学校，升学率也挺高的。请问孩子最近的成绩怎么样？

家长: [触发顾虑] 听说学校还不错，才让孩子上这个学校，这个学校的升学率怎么样？

销售: 北环中学去年的重点高中升学率在65%左右，前200名基本都能进入不错的高中...

家长: 孩子这次考试，语文89分，数学98分，但是英语只有35分，比较担心...
```

## ⚙️ 核心配置说明

### 音频配置

```javascript
// 前端：src/config/webrtc.config.js
audio: {
  sampleRate: 24000,          // 必须匹配DashScope要求
  channelCount: 1,            // 单声道
  bitRate: 24000,
  constraints: {
    echoCancellation: true,   // 回声消除（重要）
    noiseSuppression: true,   // 噪音抑制（重要）
    autoGainControl: true     // 自动增益
  }
}
```

```python
# 后端：websocket_server.py
INPUT_AUDIO_FORMAT = AudioFormat.PCM_24000HZ_MONO_16BIT
OUTPUT_AUDIO_FORMAT = AudioFormat.PCM_24000HZ_MONO_16BIT
```

### VAD配置

```python
# 后端：websocket_server.py
conversation.update_session(
    enable_turn_detection=True,         # 启用VAD
    turn_detection_type='server_vad',   # 服务端VAD
    # VAD参数在DashScope内部配置
)
```

### WebSocket配置

```javascript
// 前端
websocket: {
  url: 'ws://localhost:8080',
  reconnect: {
    maxAttempts: 5,      // 最多重连5次
    delay: 3000          // 每次延迟3秒
  },
  heartbeat: {
    interval: 30000,     // 30秒心跳
    timeout: 10000       // 10秒超时
  }
}
```

## 🔌 消息协议

### 前端 → 后端

| 消息类型 | 说明 | 频率 |
|---------|------|------|
| `session.create` | 创建会话 | 连接时一次 |
| `input_audio_buffer.append` | 发送音频 | 持续（~50次/秒） |
| `ping` | 心跳 | 30秒一次 |

### 后端 → 前端

| 消息类型 | 说明 | 用途 |
|---------|------|------|
| `session.created` | 会话创建成功 | 确认连接 |
| `response.audio.delta` | AI音频片段 | 播放AI语音 |
| `response.audio.done` | 音频完成 | 停止播放动画 |
| `conversation.item.created` | 对话转录 | 显示文本 |
| `input_audio_buffer.speech_started` | 用户开始说话 | 取消AI播放 |
| `error` | 错误信息 | 错误处理 |

## 🎨 UI功能说明

### 主界面元素

1. **状态指示器**
   - 🔴 未连接 (disconnected)
   - 🟡 连接中 (connecting)
   - 🟢 已连接 (connected)
   - 🔴 错误 (error)

2. **音频可视化**
   - 中心头像图标
   - 波纹动画（说话时）
   - 音量进度条

3. **信息卡片**
   - 通话时长
   - 连接状态
   - 音频采样率

4. **对话转录**
   - 用户发言（蓝色背景）
   - AI回复（紫色背景）
   - 自动滚动

5. **控制按钮**
   - 绿色：建立/断开连接
   - 红色：开始/停止说话
   - 灰色：静音（预留）

### 交互反馈

- ✨ 按钮悬停效果
- 🌊 录音波纹动画
- 📊 实时音量显示
- ⏱️ 通话时长计时
- 💬 实时文本转录

## 🔧 开发和调试

### 开发环境设置

```bash
# 1. 安装后端依赖
pip install -r llm/realtime/qwen/dashscope/requirements.txt

# 2. 安装前端依赖
cd ai_practice_client
npm install

# 3. 配置API Key
set DASHSCOPE_API_KEY=your_key
```

### 调试技巧

#### 后端调试

查看详细日志：
```python
# websocket_server.py
logging.basicConfig(level=logging.DEBUG)  # 改为DEBUG级别
```

#### 前端调试

启用调试模式：
```javascript
// src/config/webrtc.config.js
ui: {
  showDebug: true
}
```

查看WebSocket消息：
```
浏览器 → F12 → Network → WS → 点击连接 → Messages
```

### 性能监控

#### 音频延迟监控

```javascript
// 在VoiceCall.vue中添加
const startTime = Date.now();
// ... 发送音频
// ... 收到响应
const latency = Date.now() - startTime;
console.log('延迟:', latency, 'ms');
```

#### 内存监控

```javascript
// 浏览器控制台
console.log(performance.memory);
```

## 🚀 部署指南

### 开发环境部署

已通过启动脚本实现，见 `QUICK_START.md`

### 生产环境部署

#### 后端部署

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
export DASHSCOPE_API_KEY=your_key
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8080

# 3. 使用进程管理器运行
# 方式1: systemd
sudo systemctl start dashscope-ws

# 方式2: supervisor
supervisorctl start dashscope-ws

# 方式3: PM2 (需要安装)
pm2 start websocket_server.py --interpreter python3
```

#### 前端部署

```bash
# 1. 构建生产版本
cd ai_practice_client
npm run build

# 2. 部署dist目录到Web服务器
# nginx配置示例：
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    location / {
        root /path/to/dist;
        try_files $uri $uri/ /index.html;
    }
}

# 3. 更新WebSocket地址
# src/config/webrtc.config.js
websocket: {
  url: 'wss://your-domain.com'
}
```

### HTTPS和WSS

生产环境必须使用加密连接：

```python
# 后端添加SSL支持（使用nginx反向代理更简单）
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

async with websockets.serve(
    handle_client,
    SERVER_HOST,
    SERVER_PORT,
    ssl=ssl_context
):
    await asyncio.Future()
```

## 📊 系统性能指标

### 理论性能

- **音频延迟**: ~500ms
- **文本延迟**: ~300ms
- **并发连接**: 100+
- **音频质量**: 24kHz 16-bit

### 优化建议

1. **减少延迟**
   - 使用更小的音频缓冲（1024样本）
   - 优化网络质量
   - 使用CDN加速

2. **提高并发**
   - 使用负载均衡
   - 增加服务器实例
   - 优化数据库查询

3. **降低带宽**
   - 压缩音频数据
   - 使用更低的采样率（16kHz）
   - 减少不必要的消息

## 🔐 安全最佳实践

1. **API密钥管理**
   - 使用环境变量
   - 不提交到Git
   - 定期轮换

2. **网络安全**
   - 生产环境使用HTTPS/WSS
   - 添加访问控制
   - 实施速率限制

3. **数据安全**
   - 不记录敏感对话
   - 加密传输
   - 符合隐私法规

4. **认证授权**
   - 添加用户认证
   - 实施会话管理
   - 限制API访问

## 📈 未来扩展

### 功能扩展

- [ ] 多场景支持（面试、客服等）
- [ ] 对话历史记录
- [ ] 录音下载功能
- [ ] 实时翻译
- [ ] 情感分析
- [ ] 多语言支持

### 技术升级

- [ ] 使用AudioWorklet替代ScriptProcessorNode
- [ ] 添加单元测试
- [ ] 性能监控和分析
- [ ] 容器化部署（Docker）
- [ ] CI/CD流水线

## 📚 参考文档

- [DashScope文档](https://help.aliyun.com/zh/dashscope/)
- [WebRTC规范](https://www.w3.org/TR/webrtc/)
- [WebSocket协议](https://tools.ietf.org/html/rfc6455)
- [Vue 3文档](https://vuejs.org/)

## 🙏 致谢

感谢以下开源项目和服务：

- Vue.js团队
- DashScope团队
- WebRTC社区
- Python asyncio

---

**版本**: 1.0.0  
**更新时间**: 2025-12-23  
**许可证**: 仅供学习使用

