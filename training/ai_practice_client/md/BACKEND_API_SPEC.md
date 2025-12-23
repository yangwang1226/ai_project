# 后端WebSocket服务器接口规范

本文档定义了前端WebRTC客户端与后端服务之间的WebSocket通信协议。

## 连接信息

### WebSocket端点

```
ws://localhost:8080/ws/realtime
```

生产环境：
```
wss://api.yourdomain.com/ws/realtime
```

### 连接建立

客户端通过WebSocket连接到服务器，连接成功后：
1. 客户端发送 `session.create` 消息初始化会话
2. 服务器返回 `session.created` 确认
3. 开始音频数据传输

## 消息格式

所有消息均为JSON格式：

```json
{
  "type": "message_type",
  "data": { }
}
```

## 前端 → 后端消息

### 1. 创建会话 (session.create)

客户端请求创建新的Realtime会话。

**消息格式：**

```json
{
  "type": "session.create",
  "session": {
    "model": "gpt-4-realtime-preview",
    "modalities": ["audio", "text"],
    "voice": "alloy",
    "input_audio_format": "webm",
    "output_audio_format": "pcm16",
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 500
    },
    "temperature": 0.8,
    "max_response_output_tokens": 4096
  }
}
```

**参数说明：**

| 参数 | 类型 | 说明 |
|-----|------|------|
| model | string | 模型名称 |
| modalities | array | 支持的模态：["audio", "text"] |
| voice | string | 语音类型：alloy, echo, fable, onyx, nova, shimmer |
| input_audio_format | string | 输入音频格式：webm, pcm16, g711 |
| output_audio_format | string | 输出音频格式：pcm16, g711, mp3 |
| turn_detection | object | 语音活动检测配置 |
| temperature | number | 0-1，控制随机性 |
| max_response_output_tokens | number | 最大响应长度 |

**服务器响应：**

服务器应该：
1. 与OpenAI Realtime API建立连接
2. 创建会话
3. 返回 `session.created` 消息

---

### 2. 追加音频数据 (input_audio_buffer.append)

客户端发送实时音频数据。

**消息格式：**

```json
{
  "type": "input_audio_buffer.append",
  "audio": "base64_encoded_audio_data"
}
```

**参数说明：**

| 参数 | 类型 | 说明 |
|-----|------|------|
| audio | string | Base64编码的音频数据 |

**频率：** 每100ms发送一次

**服务器操作：**

1. 解码Base64音频数据
2. 可能需要格式转换（webm → pcm16）
3. 转发到OpenAI Realtime API

---

### 3. 提交音频缓冲 (input_audio_buffer.commit)

客户端通知服务器音频输入已完成。

**消息格式：**

```json
{
  "type": "input_audio_buffer.commit"
}
```

**服务器操作：**

将累积的音频数据提交给Realtime API处理。

---

### 4. 创建响应 (response.create)

客户端请求生成AI响应。

**消息格式：**

```json
{
  "type": "response.create",
  "response": {
    "modalities": ["audio", "text"],
    "instructions": "你是一个专业的销售助手..."
  }
}
```

**参数说明：**

| 参数 | 类型 | 说明 | 必需 |
|-----|------|------|------|
| modalities | array | 响应模态 | 否 |
| instructions | string | 特殊指令 | 否 |

---

### 5. 心跳 (ping)

客户端发送心跳保持连接。

**消息格式：**

```json
{
  "type": "ping"
}
```

**服务器响应：**

```json
{
  "type": "pong"
}
```

**频率：** 每30秒一次

---

### 6. 取消响应 (response.cancel)

客户端请求取消当前响应生成。

**消息格式：**

```json
{
  "type": "response.cancel"
}
```

---

## 后端 → 前端消息

### 1. 会话已创建 (session.created)

服务器确认会话创建成功。

**消息格式：**

```json
{
  "type": "session.created",
  "session": {
    "id": "session_123456",
    "model": "gpt-4-realtime-preview",
    "modalities": ["audio", "text"],
    "voice": "alloy",
    "created_at": 1234567890
  }
}
```

---

### 2. 音频增量数据 (response.audio.delta)

服务器发送AI生成的音频片段。

**消息格式：**

```json
{
  "type": "response.audio.delta",
  "delta": "base64_encoded_pcm16_audio",
  "response_id": "resp_123456"
}
```

**参数说明：**

| 参数 | 类型 | 说明 |
|-----|------|------|
| delta | string | Base64编码的PCM16音频数据 |
| response_id | string | 响应ID |

**频率：** 实时流式传输

**客户端操作：**

1. 解码Base64数据
2. 转换为可播放格式（如需要）
3. 播放音频

---

### 3. 音频响应完成 (response.audio.done)

服务器通知音频响应已完成。

**消息格式：**

```json
{
  "type": "response.audio.done",
  "response_id": "resp_123456"
}
```

---

### 4. 对话项已创建 (conversation.item.created)

服务器发送转录的文本内容。

**消息格式：**

```json
{
  "type": "conversation.item.created",
  "item": {
    "id": "item_123456",
    "role": "user",
    "content": [
      {
        "type": "text",
        "transcript": "你好，我想咨询一下产品信息"
      }
    ]
  }
}
```

**role类型：**
- `user` - 用户说话
- `assistant` - AI回复

---

### 5. 错误消息 (error)

服务器遇到错误时发送。

**消息格式：**

```json
{
  "type": "error",
  "error": {
    "code": "error_code",
    "message": "错误描述",
    "details": { }
  }
}
```

**常见错误码：**

| 错误码 | 说明 |
|-------|------|
| `session_not_found` | 会话不存在 |
| `invalid_audio_format` | 音频格式无效 |
| `rate_limit_exceeded` | 请求过于频繁 |
| `authentication_failed` | 认证失败 |
| `internal_error` | 内部服务器错误 |

---

### 6. 心跳响应 (pong)

服务器响应心跳。

**消息格式：**

```json
{
  "type": "pong"
}
```

---

## 连接生命周期

### 1. 建立连接

```
Client                          Server
  |                               |
  |---- WebSocket Connect ------->|
  |<------- Connected ------------|
  |                               |
  |---- session.create ---------->|
  |<----- session.created --------|
  |                               |
```

### 2. 音频交互流程

```
Client                          Server                    OpenAI Realtime API
  |                               |                               |
  |---- input_audio_buffer.append >|                              |
  |---- input_audio_buffer.append >|---- Forward Audio ---------->|
  |---- input_audio_buffer.append >|                              |
  |                               |                               |
  |---- input_audio_buffer.commit >|---- Commit Buffer ---------->|
  |---- response.create ---------->|---- Request Response ------->|
  |                               |                               |
  |<---- response.audio.delta ----|<---- Streaming Audio --------|
  |<---- response.audio.delta ----|<---- Streaming Audio --------|
  |<---- response.audio.done ------|<---- Response Complete ------|
  |                               |                               |
  |<- conversation.item.created --|<---- Transcript --------------|
  |                               |                               |
```

### 3. 关闭连接

```
Client                          Server
  |                               |
  |---- Close Connection -------->|
  |                               |-- Close Realtime API
  |<------ Closed ----------------|
  |                               |
```

---

## 音频格式转换

### 输入音频 (前端 → 后端)

**格式：** WebM (Opus编码)

**需要转换：** 如果Realtime API不支持WebM，需要转换为PCM16

**转换示例（Python）：**

```python
import base64
from pydub import AudioSegment
import io

def convert_webm_to_pcm16(webm_base64):
    # 解码Base64
    webm_data = base64.b64decode(webm_base64)
    
    # 转换为AudioSegment
    audio = AudioSegment.from_file(io.BytesIO(webm_data), format="webm")
    
    # 转换为PCM16
    pcm16 = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2)
    
    # 导出为raw PCM
    pcm_data = pcm16.raw_data
    
    return base64.b64encode(pcm_data).decode()
```

### 输出音频 (后端 → 前端)

**格式：** PCM16

**频率：** 24000 Hz

**通道：** 单声道

**比特深度：** 16位

---

## WebSocket服务器实现建议

### Node.js示例框架

```javascript
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080, path: '/ws/realtime' });

wss.on('connection', (ws) => {
  console.log('客户端已连接');
  
  let realtimeConnection = null;
  
  ws.on('message', async (message) => {
    const data = JSON.parse(message);
    
    switch(data.type) {
      case 'session.create':
        // 创建Realtime API连接
        realtimeConnection = await createRealtimeSession(data.session);
        ws.send(JSON.stringify({
          type: 'session.created',
          session: { id: 'session_123', ...data.session }
        }));
        break;
        
      case 'input_audio_buffer.append':
        // 转发音频到Realtime API
        if (realtimeConnection) {
          await forwardAudioToRealtime(realtimeConnection, data.audio);
        }
        break;
        
      case 'input_audio_buffer.commit':
        // 提交音频
        if (realtimeConnection) {
          await commitAudioBuffer(realtimeConnection);
        }
        break;
        
      case 'response.create':
        // 请求响应
        if (realtimeConnection) {
          await createResponse(realtimeConnection);
        }
        break;
        
      case 'ping':
        ws.send(JSON.stringify({ type: 'pong' }));
        break;
    }
  });
  
  ws.on('close', () => {
    console.log('客户端已断开');
    if (realtimeConnection) {
      realtimeConnection.close();
    }
  });
});
```

### Python示例框架

```python
import asyncio
import websockets
import json

async def handle_client(websocket, path):
    realtime_connection = None
    
    async for message in websocket:
        data = json.loads(message)
        
        if data['type'] == 'session.create':
            # 创建Realtime API连接
            realtime_connection = await create_realtime_session(data['session'])
            await websocket.send(json.dumps({
                'type': 'session.created',
                'session': {'id': 'session_123', **data['session']}
            }))
            
        elif data['type'] == 'input_audio_buffer.append':
            # 转发音频
            if realtime_connection:
                await forward_audio_to_realtime(realtime_connection, data['audio'])
                
        elif data['type'] == 'ping':
            await websocket.send(json.dumps({'type': 'pong'}))

start_server = websockets.serve(handle_client, 'localhost', 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

---

## 安全建议

1. **认证**：在连接建立时验证客户端身份
2. **速率限制**：限制消息发送频率
3. **数据验证**：验证所有输入数据
4. **错误处理**：优雅地处理所有错误情况
5. **日志记录**：记录所有重要操作
6. **超时处理**：设置合理的超时时间

## 性能优化

1. **音频缓冲**：适当缓冲音频数据减少网络请求
2. **并发控制**：限制同时连接数
3. **资源清理**：及时释放不用的资源
4. **连接池**：复用与Realtime API的连接

---

## 测试工具

### WebSocket测试工具

1. **Postman** - 支持WebSocket测试
2. **wscat** - 命令行WebSocket客户端
3. **WebSocket King** - Chrome扩展

### 测试命令示例（wscat）

```bash
# 安装wscat
npm install -g wscat

# 连接到服务器
wscat -c ws://localhost:8080/ws/realtime

# 发送消息
> {"type":"session.create","session":{"model":"gpt-4-realtime-preview"}}
```

---

## 常见问题

### Q: 如何处理音频格式转换？

A: 可以使用FFmpeg、pydub（Python）或fluent-ffmpeg（Node.js）进行转换。

### Q: 如何优化音频传输延迟？

A: 
- 减小音频块大小
- 使用更快的编码格式
- 优化网络带宽
- 使用WebSocket压缩

### Q: 如何处理网络断开？

A: 
- 实现重连机制
- 保存会话状态
- 使用心跳检测
- 设置合理的超时时间

---

需要更多帮助？请参考：
- [OpenAI Realtime API文档](https://platform.openai.com/docs/api-reference/realtime)
- [WebSocket协议规范](https://tools.ietf.org/html/rfc6455)
- [WebRTC API文档](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)

