# 调试日志说明

## 📊 后端日志（Python控制台）

### 连接相关
```
INFO - [session_xxx] Client connected from ('127.0.0.1', xxxx)
INFO - [session_xxx] DashScope connection opened
INFO - [session_xxx] Session created with voice: Cherry
```

### 音频接收
```
INFO - [session_xxx] ✅ Received audio data: 2732 bytes
INFO - [session_xxx] ✅ Received audio data: 2732 bytes
...（持续接收）
```
**说明**: 每次前端发送音频数据时都会打印，显示接收到的Base64编码音频字节数

### VAD检测
```
[session_xxx] ======VAD: 检测到用户开始说话======
[session_xxx] ======VAD: 检测到用户停止说话======
```
**说明**: DashScope的服务端VAD自动检测用户说话状态

### 用户语音转录
```
[session_xxx] 🎤 用户说: 家长您好，我是新东方的课程顾问
```
**说明**: 显示用户说话的完整转录文本

### AI响应
```
[session_xxx] 🤖 AI回复增量: 您
[session_xxx] 🤖 AI回复增量: 好
[session_xxx] 🤖 AI回复增量: ，
[session_xxx] 🤖 AI回复增量: 我
...（流式输出）
```
**说明**: AI回复的文本增量，实时流式输出

### AI完整回复
```
[session_xxx] ======响应完成======
[session_xxx] 📝 AI完整回复: 您好，我想了解一下新东方这边的培训课程？
```
**说明**: 响应完成后显示AI的完整回复文本

### 音频发送（DEBUG级别）
```
DEBUG - [session_xxx] 🔊 Sending audio delta: 4096 bytes
```
**说明**: 发送给前端的音频数据大小（需要设置日志级别为DEBUG才能看到）

---

## 🌐 前端日志（浏览器控制台 F12）

### 连接建立
```
WebSocket连接已建立
服务初始化成功
```

### 录音开始
```
开始PCM录音, 采样率: 24000
```

### 音频发送
```
🎤 发送音频数据: 2732 bytes
🎤 发送音频数据: 2732 bytes
...（持续发送）
```
**说明**: 每次发送音频数据到后端时打印

### 接收服务器消息
```
📥 收到服务器消息: {"type":"session.created","session":{"id":"session_xxx"...
📥 收到服务器消息: {"type":"response.audio.delta","delta":"base64_audio_data"...
📥 收到服务器消息: {"type":"conversation.item.created","item":{"role":"user"...
```
**说明**: 显示从服务器接收到的所有消息（前100个字符）

---

## 🔍 完整对话流程日志示例

### 1. 建立连接
```
【前端】WebSocket连接已建立
【后端】INFO - [session_123] Client connected from ('127.0.0.1', 54321)
【后端】INFO - [session_123] DashScope connection opened
【后端】INFO - [session_123] Session created with voice: Cherry
【前端】📥 收到服务器消息: {"type":"session.created"...
```

### 2. 开始说话
```
【前端】开始PCM录音, 采样率: 24000
【前端】🎤 发送音频数据: 2732 bytes
【后端】INFO - [session_123] ✅ Received audio data: 2732 bytes
【前端】🎤 发送音频数据: 2732 bytes
【后端】INFO - [session_123] ✅ Received audio data: 2732 bytes
...（持续）
```

### 3. VAD检测到说话
```
【后端】[session_123] ======VAD: 检测到用户开始说话======
【前端】📥 收到服务器消息: {"type":"input_audio_buffer.speech_started"...
```

### 4. 停止说话
```
【后端】[session_123] ======VAD: 检测到用户停止说话======
【前端】📥 收到服务器消息: {"type":"input_audio_buffer.speech_stopped"...
```

### 5. 语音识别结果
```
【后端】[session_123] 🎤 用户说: 家长您好，我是新东方的课程顾问
【前端】📥 收到服务器消息: {"type":"conversation.item.created","item":{"role":"user"...
```

### 6. AI开始回复
```
【后端】[session_123] 🤖 AI回复增量: 您
【后端】[session_123] 🤖 AI回复增量: 好
【后端】[session_123] 🤖 AI回复增量: ，
【后端】[session_123] 🤖 AI回复增量: 我
【后端】[session_123] 🤖 AI回复增量: 想
【后端】[session_123] 🤖 AI回复增量: 了
【后端】[session_123] 🤖 AI回复增量: 解
...
【前端】📥 收到服务器消息: {"type":"response.audio.delta"...
【前端】📥 收到服务器消息: {"type":"response.audio.delta"...
...
```

### 7. 响应完成
```
【后端】[session_123] ======响应完成======
【后端】[session_123] 📝 AI完整回复: 您好，我想了解一下新东方这边的培训课程？
【前端】📥 收到服务器消息: {"type":"response.audio.done"...
【前端】📥 收到服务器消息: {"type":"conversation.item.created","item":{"role":"assistant"...
```

---

## 🐛 常见问题诊断

### 问题1: 没有"✅ Received audio data"日志

**可能原因**:
- 前端没有发送音频数据
- WebSocket连接断开
- 前端录音失败

**检查**:
1. 查看前端是否有 `🎤 发送音频数据` 日志
2. 检查浏览器控制台是否有错误
3. 确认麦克风权限已授予

### 问题2: 有音频数据但没有VAD检测

**可能原因**:
- 音频太小声
- 音频格式不正确
- VAD阈值设置问题

**检查**:
1. 确认音频数据持续发送（不是只发送一两次）
2. 检查采样率是否为24000Hz
3. 尝试大声说话

### 问题3: 有VAD但没有转录结果

**可能原因**:
- 说话时间太短
- 音频质量问题
- API配置问题

**检查**:
1. 确认说话时间超过1秒
2. 检查后端是否有错误日志
3. 验证API Key是否有效

### 问题4: 有转录但没有AI回复

**可能原因**:
- 提示词问题
- API额度不足
- 网络问题

**检查**:
1. 查看后端是否有error日志
2. 检查API Key额度
3. 确认网络连接正常

---

## 🔧 启用DEBUG级别日志

如果需要更详细的日志，可以修改后端日志级别：

```python
# websocket_server.py
logging.basicConfig(
    level=logging.DEBUG,  # 改为DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

这将显示：
- 所有WebSocket消息的详细内容
- 音频数据的详细信息
- DashScope API的详细交互

---

## 📝 日志符号说明

| 符号 | 含义 |
|-----|------|
| ✅ | 成功接收/发送 |
| 🎤 | 用户语音相关 |
| 🤖 | AI回复相关 |
| 🔊 | 音频数据 |
| 📝 | 文本内容 |
| 📥 | 接收消息 |
| ⚠️ | 警告 |
| ❌ | 错误 |

---

## 🎯 测试建议

1. **启动后端**，观察是否有 "WebSocket server started successfully"
2. **打开前端**，观察浏览器控制台
3. **点击"建立连接"**，观察两端的连接日志
4. **点击"开始说话"**，观察是否有 "开始PCM录音" 和 "发送音频数据"
5. **说话测试**，说 "家长您好，我是新东方的课程顾问"
6. **观察后端**，应该看到：
   - ✅ Received audio data（持续）
   - ======VAD: 检测到用户开始说话======
   - ======VAD: 检测到用户停止说话======
   - 🎤 用户说: xxx
   - 🤖 AI回复增量: xxx
   - 📝 AI完整回复: xxx

如果某个环节没有日志，说明问题出在该环节之前。

---

**提示**: 保持后端和前端的控制台都打开，这样可以同时看到两端的日志，更容易定位问题！

