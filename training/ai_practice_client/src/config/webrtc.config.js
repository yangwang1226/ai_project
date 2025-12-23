/**
 * WebRTC和WebSocket配置
 */

export const WebRTCConfig = {
  // WebSocket服务器配置
  websocket: {
    // 开发环境URL - 连接到本地DashScope WebSocket服务器
    development: 'ws://localhost:8080',
    // 生产环境URL
    production: 'wss://your-production-domain.com',
    // 当前环境
    url: process.env.NODE_ENV === 'production' 
      ? 'wss://your-production-domain.com'
      : 'ws://localhost:8080',
    // 重连配置
    reconnect: {
      maxAttempts: 5,
      delay: 3000
    },
    // 心跳配置
    heartbeat: {
      interval: 30000,
      timeout: 10000
    }
  },

  // 音频配置
  audio: {
    // 采样率（Hz） - DashScope使用24kHz
    sampleRate: 24000,
    // 通道数
    channelCount: 1,
    // 比特率（bps）
    bitRate: 24000,
    // 音频处理选项
    constraints: {
      echoCancellation: true,  // 回声消除
      noiseSuppression: true,  // 噪音抑制
      autoGainControl: true    // 自动增益控制
    },
    // 支持的音频格式（按优先级排序）
    mimeTypes: [
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/ogg;codecs=opus',
      'audio/mp4'
    ]
  },

  // Realtime API配置（DashScope Qwen-Omni）
  realtimeAPI: {
    // 模型配置
    model: 'qwen3-omni-flash-realtime',
    // 支持的模态
    modalities: ['audio', 'text'],
    // 语音选项 - DashScope支持的语音
    voice: 'Cherry', // 可选: Cherry 等
    // 输入音频格式
    inputAudioFormat: 'pcm16',
    // 输出音频格式
    outputAudioFormat: 'pcm16',
    // 语音活动检测(VAD)配置
    turnDetection: {
      type: 'server_vad',      // 服务端VAD
      threshold: 0.5,          // 检测阈值 (0-1)
      prefixPaddingMs: 300,    // 前缀填充时间(ms)
      silenceDurationMs: 500   // 静音持续时间(ms)
    },
    // 温度参数（0-1，值越高输出越随机）
    temperature: 0.8,
    // 最大响应长度
    maxResponseOutputTokens: 4096
  },

  // UI配置
  ui: {
    // 是否显示调试信息
    showDebug: false,
    // 音量更新频率(ms)
    volumeUpdateInterval: 100,
    // 音频数据发送频率(ms)
    audioChunkInterval: 100
  }
};

export default WebRTCConfig;

