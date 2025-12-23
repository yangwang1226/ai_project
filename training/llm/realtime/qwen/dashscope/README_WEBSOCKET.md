# WebSocket服务器使用说明

## 概述

这是一个将阿里云DashScope Realtime API包装成WebSocket服务器的实现，用于支持前端WebRTC客户端进行实时语音对话。

## 文件说明

- `websocket_server.py` - WebSocket服务器主程序
- `prompts/sales_training.txt` - 默认的系统提示词（销售培训场景）
- `run_server_vad.py` - 原始的命令行客户端（已更新为使用独立的提示词文件）
- `requirements.txt` - Python依赖包

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API Key

设置环境变量：

```bash
# Windows
set DASHSCOPE_API_KEY=your_api_key_here

# Linux/Mac
export DASHSCOPE_API_KEY=your_api_key_here
```

或者直接在 `websocket_server.py` 中修改硬编码的API Key。

### 3. 启动服务器

```bash
cd c:\workspace\ai_project\training
python llm\realtime\qwen\dashscope\websocket_server.py
```

服务器将在 `0.0.0.0:8080` 上启动。

### 4. 启动前端

```bash
cd ai_practice_client
npm run dev
```

访问 `http://localhost:5173/voice-call` 开始语音对话。

## 架构说明

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│   前端Vue   │         │  WebSocket服务器  │         │  DashScope  │
│   WebRTC    │<------->│  (Python)        │<------->│   Realtime  │
│   客户端    │         │  websocket_server│         │     API     │
└─────────────┘         └──────────────────┘         └─────────────┘
```

### 数据流

1. **前端 → WebSocket服务器**：
   - 发送 `session.create` 创建会话
   - 持续发送音频数据 `input_audio_buffer.append`

2. **WebSocket服务器 → DashScope**：
   - 建立Realtime连接
   - 转发音频数据
   - 配置VAD和语音参数

3. **DashScope → WebSocket服务器 → 前端**：
   - 返回音频响应 `response.audio.delta`
   - 返回文本转录 `conversation.item.created`
   - VAD事件通知

## 音频格式

- **采样率**: 24000 Hz
- **通道**: 单声道 (Mono)
- **位深度**: 16-bit
- **格式**: PCM

前端使用MediaRecorder录制音频，后端接收Base64编码的音频数据。

## 消息协议

### 前端 → 服务器

#### 创建会话
```json
{
  "type": "session.create",
  "session": {
    "model": "qwen3-omni-flash-realtime",
    "voice": "Cherry",
    "instructions": "可选的自定义提示词"
  }
}
```

#### 发送音频
```json
{
  "type": "input_audio_buffer.append",
  "audio": "base64_encoded_audio_data"
}
```

#### 心跳
```json
{
  "type": "ping"
}
```

### 服务器 → 前端

#### 会话已创建
```json
{
  "type": "session.created",
  "session": {
    "id": "session_xxx",
    "model": "qwen3-omni-flash-realtime"
  }
}
```

#### 音频响应
```json
{
  "type": "response.audio.delta",
  "delta": "base64_encoded_pcm_audio",
  "response_id": "resp_xxx"
}
```

#### 文本转录（用户）
```json
{
  "type": "conversation.item.created",
  "item": {
    "role": "user",
    "content": [{
      "type": "text",
      "transcript": "用户说的话"
    }]
  }
}
```

#### 文本转录（AI）
```json
{
  "type": "conversation.item.created",
  "item": {
    "role": "assistant",
    "content": [{
      "type": "text",
      "transcript": "AI的回复"
    }]
  }
}
```

#### 响应完成
```json
{
  "type": "response.audio.done",
  "response_id": "resp_xxx"
}
```

#### 错误
```json
{
  "type": "error",
  "error": {
    "code": "error_code",
    "message": "错误描述"
  }
}
```

## 自定义提示词

### 使用默认提示词

默认使用 `prompts/sales_training.txt` 中的销售培训场景提示词。

### 自定义提示词

有两种方式：

#### 方式1: 修改提示词文件

直接编辑 `prompts/sales_training.txt` 文件，修改提示词内容。

#### 方式2: 在创建会话时传递

前端发送 `session.create` 时包含 `instructions` 字段：

```javascript
wsService.value.send({
  type: 'session.create',
  session: {
    model: 'qwen3-omni-flash-realtime',
    voice: 'Cherry',
    instructions: '你是一个友好的AI助手...'  // 自定义提示词
  }
});
```

## 日志

服务器会输出详细的日志信息：

- `INFO` - 正常的操作日志（连接、会话创建等）
- `DEBUG` - 详细的调试信息（消息收发）
- `ERROR` - 错误信息
- `WARNING` - 警告信息

## 故障排查

### 1. 连接失败

**问题**: 前端显示"连接错误"

**解决**:
- 检查WebSocket服务器是否已启动
- 检查防火墙设置
- 确认端口8080没有被占用

### 2. API Key错误

**问题**: 服务器日志显示认证失败

**解决**:
- 检查 `DASHSCOPE_API_KEY` 环境变量是否正确设置
- 或在代码中更新API Key

### 3. 音频无法播放

**问题**: 收到音频数据但无法播放

**解决**:
- 检查浏览器控制台错误
- 确认音频格式匹配（24kHz PCM16）
- 检查浏览器是否支持音频播放

### 4. 转录不准确

**问题**: 语音识别结果不准确

**解决**:
- 确保麦克风质量良好
- 在安静的环境中使用
- 说话清晰，语速适中

## 性能优化

1. **音频缓冲**: 前端每100ms发送一次音频数据，平衡延迟和流畅度
2. **异步处理**: 使用asyncio处理并发连接
3. **日志级别**: 生产环境可以将日志级别设置为WARNING

## 安全建议

1. **API Key安全**: 不要将API Key提交到版本控制
2. **访问控制**: 生产环境应添加认证机制
3. **速率限制**: 建议添加请求频率限制
4. **HTTPS**: 生产环境使用WSS（WebSocket over TLS）

## 扩展功能

### 添加新的提示词场景

在 `prompts/` 目录下创建新的txt文件，例如 `customer_service.txt`：

```python
# 在websocket_server.py中修改
DEFAULT_PROMPT_FILE = './llm/realtime/qwen/dashscope/prompts/customer_service.txt'
```

### 支持多个并发会话

当前实现已支持多个客户端同时连接，每个连接都有独立的会话ID和状态。

### 添加会话历史

可以扩展 `SessionManager` 类来保存会话历史：

```python
class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.history = {}  # 添加历史记录
```

## 参考资料

- [DashScope文档](https://help.aliyun.com/zh/dashscope/)
- [WebSocket协议](https://tools.ietf.org/html/rfc6455)
- [WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)

## 许可证

仅供学习使用。

