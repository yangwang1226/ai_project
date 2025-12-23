# 快速启动指南

## 🚀 一键启动整个系统

### 系统架构

```
前端 (Vue + WebRTC)  ←→  后端 (Python WebSocket)  ←→  DashScope API
     localhost:5173            localhost:8080              云端服务
```

## 📋 前置要求

### 1. Node.js 环境
- Node.js 16+ 
- npm 或 pnpm

### 2. Python 环境
- Python 3.8+
- pip

### 3. DashScope API Key
- 需要有效的阿里云DashScope API密钥

## ⚡ 快速启动步骤

### 方式一：使用启动脚本（推荐）

#### 1. 安装Python依赖

```bash
cd c:\workspace\ai_project\training
pip install -r llm\realtime\qwen\dashscope\requirements.txt
```

#### 2. 启动后端服务器

双击运行：`start_backend.bat`

或在命令行中：
```bash
start_backend.bat
```

**输出示例：**
```
========================================
Starting WebSocket Backend Server
========================================

Starting server on localhost:8080...
INFO - Starting WebSocket server on 0.0.0.0:8080
INFO - WebSocket server started successfully
```

#### 3. 启动前端开发服务器

**新开一个命令行窗口**，双击运行：`start_frontend.bat`

或在命令行中：
```bash
start_frontend.bat
```

**输出示例：**
```
========================================
Starting Frontend Development Server
========================================

  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

#### 4. 打开浏览器

访问：`http://localhost:5173/voice-call`

---

### 方式二：手动启动

#### 后端启动

```bash
# 1. 进入项目根目录
cd c:\workspace\ai_project\training

# 2. 安装依赖
pip install -r llm\realtime\qwen\dashscope\requirements.txt

# 3. 设置API Key（可选）
set DASHSCOPE_API_KEY=your_api_key_here

# 4. 启动服务器
python llm\realtime\qwen\dashscope\websocket_server.py
```

#### 前端启动

**新开一个命令行窗口：**

```bash
# 1. 进入前端目录
cd c:\workspace\ai_project\training\ai_practice_client

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

## 🎯 使用步骤

### 1. 打开语音通话页面

在浏览器中访问：`http://localhost:5173/voice-call`

### 2. 允许麦克风权限

首次访问时，浏览器会请求麦克风权限，点击"允许"。

### 3. 建立连接

点击页面上的"建立连接"按钮。

**成功标志：**
- 状态指示灯变绿
- 显示"已连接"

### 4. 开始对话

点击"开始说话"按钮（红色录音按钮），开始说话。

**功能说明：**
- 🎤 音量条会实时显示你的说话音量
- 💬 你的话会实时转录显示
- 🤖 AI会自动回复（语音+文字）
- 📊 通话时长自动计时

### 5. 结束对话

- 点击"停止说话"停止当前输入
- 点击"断开连接"结束整个会话

## 🎭 默认场景说明

系统默认使用**销售培训场景**：

- **AI角色**：咨询课程的学生家长
- **你的角色**：新东方的销售人员
- **任务**：练习销售技巧，回答家长的问题

**对话开始要求：**
必须以"家长您好"开头，否则AI会提示你。

**示例对话：**
```
你: 家长您好，我是新东方的课程顾问，请问有什么可以帮您的？
AI: 您好，我想了解一下新东方这边的培训课程？
你: 好的，请问孩子现在几年级了？
AI: 七年级
...
```

## ⚙️ 配置说明

### 修改API Key

**方式1：环境变量（推荐）**
```bash
set DASHSCOPE_API_KEY=your_api_key_here
```

**方式2：修改代码**
编辑 `llm\realtime\qwen\dashscope\websocket_server.py`：
```python
dashscope.api_key = 'your_api_key_here'
```

### 修改提示词

编辑文件：`llm\realtime\qwen\dashscope\prompts\sales_training.txt`

你可以修改AI的角色、任务、对话规则等。

### 修改语音

编辑 `ai_practice_client\src\config\webrtc.config.js`：
```javascript
realtimeAPI: {
  voice: 'Cherry', // 修改为其他支持的语音
}
```

DashScope支持的语音选项：Cherry等（查看官方文档了解更多）

### 修改端口

**后端端口**：编辑 `websocket_server.py`：
```python
SERVER_PORT = 8080  # 修改为其他端口
```

**前端配置**：编辑 `src/config/webrtc.config.js`：
```javascript
websocket: {
  url: 'ws://localhost:8080', // 修改为对应端口
}
```

## 🔍 故障排查

### 问题1：后端启动失败

**错误：** `ModuleNotFoundError: No module named 'dashscope'`

**解决：**
```bash
pip install dashscope websockets pyaudio
```

### 问题2：前端连接失败

**错误：** 页面显示"连接错误"

**检查清单：**
1. ✅ 后端服务器是否已启动？
2. ✅ 端口8080是否被占用？
3. ✅ 防火墙是否阻止了连接？

**解决：**
- 查看后端控制台是否有错误信息
- 确认后端显示"WebSocket server started successfully"
- 检查浏览器控制台的错误信息

### 问题3：无法录音

**错误：** "无法访问麦克风"

**解决：**
1. 检查浏览器麦克风权限
2. 检查系统麦克风设置
3. 确保麦克风设备正常工作

### 问题4：API Key错误

**错误：** 后端日志显示认证失败

**解决：**
1. 检查API Key是否正确
2. 确认API Key有足够的额度
3. 访问阿里云控制台验证API Key状态

### 问题5：音频无法播放

**错误：** 收到响应但没有声音

**解决：**
1. 检查系统音量设置
2. 检查浏览器音频权限
3. 查看浏览器控制台是否有音频播放错误

## 📊 系统监控

### 后端日志

后端会输出详细日志：
```
INFO - [session_xxx] Client connected
INFO - [session_xxx] Session created with voice: Cherry
INFO - [session_xxx] User said: 家长您好，请问有什么可以帮您？
INFO - [session_xxx] Response done
```

### 前端调试

打开浏览器开发者工具（F12）：
- **Console**：查看连接状态和错误
- **Network → WS**：查看WebSocket消息收发

### 启用调试模式

编辑 `src/views/VoiceCall.vue`，找到：
```javascript
const showDebug = ref(WebRTCConfig.ui.showDebug);
```

或直接在配置文件 `src/config/webrtc.config.js` 中设置：
```javascript
ui: {
  showDebug: true,  // 改为true
}
```

页面底部会显示详细的调试信息。

## 📱 浏览器兼容性

| 浏览器 | 支持情况 | 建议版本 |
|-------|---------|---------|
| Chrome | ✅ 完全支持 | 74+ |
| Edge | ✅ 完全支持 | 79+ |
| Firefox | ✅ 支持 | 66+ |
| Safari | ⚠️ 部分支持 | 12+ |
| IE | ❌ 不支持 | - |

**推荐使用 Chrome 浏览器**

## 🔐 安全提示

1. **不要将API Key提交到Git**
2. **使用环境变量存储敏感信息**
3. **生产环境使用HTTPS和WSS**
4. **定期更新依赖包**

## 📚 更多文档

- **前端集成指南**：`ai_practice_client/INTEGRATION_GUIDE.md`
- **WebSocket后端文档**：`llm/realtime/qwen/dashscope/README_WEBSOCKET.md`
- **项目结构说明**：`ai_practice_client/PROJECT_STRUCTURE.md`

## 🆘 获取帮助

遇到问题？

1. 查看日志输出
2. 检查浏览器控制台
3. 参考故障排查部分
4. 查阅详细文档

---

**祝你使用愉快！** 🎉

如果一切正常，你现在应该可以和AI进行实时语音对话了！

