<template>
  <div class="voice-call-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <button class="back-btn" @click="goBack">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <h1 class="title">实时语音通话</h1>
      <div class="status-indicator" :class="connectionStatus">
        <span class="status-dot"></span>
        <span class="status-text">{{ statusText }}</span>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- 音频可视化区域 -->
      <div class="audio-visualizer">
        <div class="avatar-container">
          <div class="avatar" :class="{ active: isRecording || isSpeaking }">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" 
                    fill="currentColor"/>
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" 
                    fill="currentColor"/>
            </svg>
          </div>
          
          <!-- 音量波纹效果 -->
          <div class="wave-ring" v-if="isRecording" :style="{ transform: `scale(${1 + volumeLevel / 100})` }"></div>
          <div class="wave-ring wave-ring-2" v-if="isRecording" :style="{ transform: `scale(${1.2 + volumeLevel / 80})` }"></div>
          <div class="wave-ring wave-ring-3" v-if="isRecording" :style="{ transform: `scale(${1.4 + volumeLevel / 60})` }"></div>
        </div>

        <!-- 音量指示器 -->
        <div class="volume-indicator">
          <div class="volume-bar">
            <div class="volume-fill" :style="{ width: volumeLevel + '%' }"></div>
          </div>
          <span class="volume-text">音量: {{ Math.round(volumeLevel) }}%</span>
        </div>
      </div>

      <!-- 对话信息显示 -->
      <div class="conversation-info">
        <div class="info-card">
          <div class="info-row">
            <span class="info-label">通话时长:</span>
            <span class="info-value">{{ formattedDuration }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">连接状态:</span>
            <span class="info-value" :class="connectionStatus">{{ statusText }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">采样率:</span>
            <span class="info-value">{{ sampleRate }} Hz</span>
          </div>
        </div>

        <!-- 实时转录文本 -->
        <div class="transcript-card" v-if="transcript.length > 0">
          <h3>对话内容</h3>
          <div class="transcript-list">
            <div v-for="(item, index) in transcript" :key="index" 
                 class="transcript-item" :class="item.role">
              <span class="speaker">{{ item.role === 'user' ? '我' : 'AI' }}:</span>
              <span class="text">{{ item.text }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 控制按钮区域 -->
      <div class="controls">
        <button 
          class="control-btn connect-btn" 
          @click="toggleConnection"
          :disabled="isConnecting">
          <svg v-if="!isConnected" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z" 
                  fill="currentColor"/>
          </svg>
          <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" 
                  fill="currentColor"/>
          </svg>
          <span>{{ isConnected ? '断开连接' : '建立连接' }}</span>
        </button>

        <button 
          class="control-btn record-btn" 
          :class="{ active: isRecording }"
          @click="toggleRecording"
          :disabled="!isConnected">
          <svg v-if="!isRecording" width="32" height="32" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="8" fill="currentColor"/>
          </svg>
          <svg v-else width="32" height="32" viewBox="0 0 24 24" fill="none">
            <rect x="6" y="6" width="12" height="12" fill="currentColor" rx="2"/>
          </svg>
          <span>{{ isRecording ? '停止说话' : '开始说话' }}</span>
        </button>

        <button 
          class="control-btn mute-btn" 
          @click="toggleMute"
          :disabled="!isConnected">
          <svg v-if="!isMuted" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z" 
                  fill="currentColor"/>
          </svg>
          <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z" 
                  fill="currentColor"/>
          </svg>
          <span>{{ isMuted ? '取消静音' : '静音' }}</span>
        </button>
      </div>

      <!-- 调试信息（开发模式） -->
      <div class="debug-panel" v-if="showDebug">
        <h4>调试信息</h4>
        <pre>{{ debugInfo }}</pre>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import WebRTCService from '../services/webrtc.js';
import WebSocketService from '../services/websocket.js';
import WebRTCConfig from '../config/webrtc.config.js';

export default {
  name: 'VoiceCall',
  setup() {
    const router = useRouter();

    // 服务实例
    const webrtcService = ref(null);
    const wsService = ref(null);

    // 连接状态
    const isConnected = ref(false);
    const isConnecting = ref(false);
    const connectionStatus = ref('disconnected'); // disconnected, connecting, connected, error

    // 录音状态
    const isRecording = ref(false);
    const isMuted = ref(false);
    const isSpeaking = ref(false);

    // 音频数据
    const volumeLevel = ref(0);
    const sampleRate = ref(24000);

    // 通话数据
    const callStartTime = ref(null);
    const callDuration = ref(0);
    const transcript = ref([]);
    
    // 音频缓冲
    const audioChunks = ref([]);

    // 调试
    const showDebug = ref(WebRTCConfig.ui.showDebug); // 从配置文件读取

    // WebSocket配置
    const WS_URL = WebRTCConfig.websocket.url; // 从配置文件读取

    // 计算属性
    const statusText = computed(() => {
      const statusMap = {
        'disconnected': '未连接',
        'connecting': '连接中...',
        'connected': '已连接',
        'reconnecting': '重新连接中...',
        'error': '连接错误'
      };
      return statusMap[connectionStatus.value] || '未知';
    });

    const formattedDuration = computed(() => {
      const minutes = Math.floor(callDuration.value / 60);
      const seconds = callDuration.value % 60;
      return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    });

    const debugInfo = computed(() => {
      if (!webrtcService.value || !wsService.value) return {};
      
      return {
        webrtc: webrtcService.value.getStatus(),
        websocket: {
          readyState: wsService.value.getReadyState(),
          reconnectAttempts: wsService.value.reconnectAttempts
        },
        call: {
          isRecording: isRecording.value,
          volumeLevel: Math.round(volumeLevel.value),
          duration: callDuration.value
        }
      };
    });

    // 初始化服务
    const initializeServices = async () => {
      try {
        // 初始化WebRTC服务
        webrtcService.value = new WebRTCService();
        await webrtcService.value.initialize();

        // 设置音量监听
        webrtcService.value.onVolumeChange((level) => {
          volumeLevel.value = level;
        });

        // 获取采样率
        const status = webrtcService.value.getStatus();
        if (status.sampleRate) {
          sampleRate.value = status.sampleRate;
        }

        console.log('服务初始化成功');
      } catch (error) {
        console.error('初始化服务失败:', error);
        alert('初始化音频失败: ' + error.message);
      }
    };

    // 建立WebSocket连接
    const connectWebSocket = async () => {
      try {
        isConnecting.value = true;
        connectionStatus.value = 'connecting';

        // 初始化WebSocket服务
        wsService.value = new WebSocketService();

        // 监听连接状态变化
        wsService.value.onConnectionStateChange((state) => {
          connectionStatus.value = state;
          isConnected.value = state === 'connected';
        });

        // 注册消息处理器
        setupMessageHandlers();

        // 连接到服务器
        await wsService.value.connect(WS_URL);

        // 发送初始化消息（使用配置文件）
        wsService.value.send({
          type: 'session.create',
          session: {
            model: WebRTCConfig.realtimeAPI.model,
            modalities: WebRTCConfig.realtimeAPI.modalities,
            voice: WebRTCConfig.realtimeAPI.voice,
            input_audio_format: WebRTCConfig.realtimeAPI.inputAudioFormat,
            output_audio_format: WebRTCConfig.realtimeAPI.outputAudioFormat,
            turn_detection: {
              type: WebRTCConfig.realtimeAPI.turnDetection.type,
              threshold: WebRTCConfig.realtimeAPI.turnDetection.threshold,
              prefix_padding_ms: WebRTCConfig.realtimeAPI.turnDetection.prefixPaddingMs,
              silence_duration_ms: WebRTCConfig.realtimeAPI.turnDetection.silenceDurationMs
            }
          }
        });

        callStartTime.value = Date.now();
        startDurationTimer();

      } catch (error) {
        console.error('连接WebSocket失败:', error);
        connectionStatus.value = 'error';
        alert('连接服务器失败: ' + error.message);
      } finally {
        isConnecting.value = false;
      }
    };

    // 设置消息处理器
    const setupMessageHandlers = () => {
      // 处理会话创建响应
      wsService.value.on('session.created', (message) => {
        console.log('会话已创建:', message);
      });

      // 处理音频响应增量
      wsService.value.on('response.audio.delta', (message) => {
        if (message.delta) {
          console.log('🔊 收到音频增量 #' + (audioChunks.value.length + 1) + ':', message.delta.length, 'bytes');
          // 累积音频数据
          isSpeaking.value = true;
          audioChunks.value.push(message.delta);
        } else {
          console.warn('⚠️ 收到空的音频delta');
        }
      });

      // 处理音频响应完成
      wsService.value.on('response.audio.done', async () => {
        console.log('✅ 音频接收完成，开始播放...');
        isSpeaking.value = false;
        
        // 合并所有音频片段并播放
        if (audioChunks.value.length > 0) {
          try {
            await playAllAudioChunks();
          } catch (error) {
            console.error('播放音频失败:', error);
          }
        }
      });

      // 处理VAD - 用户开始说话
      wsService.value.on('input_audio_buffer.speech_started', () => {
        console.log('🎤 用户开始说话，清空音频缓冲');
        audioChunks.value = [];  // 清空之前的音频缓冲
      });

      // 处理转录结果
      wsService.value.on('conversation.item.created', (message) => {
        console.log('📝 收到转录:', message);
        if (message.item && message.item.content) {
          const content = message.item.content[0];
          if (content.transcript) {
            transcript.value.push({
              role: message.item.role,
              text: content.transcript
            });
            console.log(`✅ 添加${message.item.role}的对话:`, content.transcript);
          }
        }
      });

      // 处理错误
      wsService.value.on('error', (message) => {
        console.error('服务器错误:', message);
        alert('服务器错误: ' + message.error?.message);
      });

      // 监听所有消息（用于调试）
      // wsService.value.on('*', (message) => {
      //   console.log('收到消息:', message);
      // });
    };

    // 播放所有音频片段
    const playAllAudioChunks = async () => {
      if (audioChunks.value.length === 0) {
        console.warn('⚠️ 没有音频数据可播放');
        return;
      }
      
      try {
        console.log('🎵 准备播放', audioChunks.value.length, '个音频片段');
        console.log('🎵 第一个片段长度:', audioChunks.value[0]?.length || 0);
        
        // 将所有base64片段解码并合并
        const allPcmData = [];
        for (let i = 0; i < audioChunks.value.length; i++) {
          const chunk = audioChunks.value[i];
          try {
            // 解码base64
            const binaryString = atob(chunk);
            const bytes = new Uint8Array(binaryString.length);
            for (let j = 0; j < binaryString.length; j++) {
              bytes[j] = binaryString.charCodeAt(j);
            }
            // 转换为Int16
            const int16Array = new Int16Array(bytes.buffer);
            allPcmData.push(...int16Array);
            
            if (i === 0) {
              console.log('🎵 第一个片段解码后长度:', int16Array.length, '个采样点');
            }
          } catch (err) {
            console.error(`🔴 解码第${i}个片段失败:`, err);
          }
        }
        
        if (allPcmData.length === 0) {
          console.error('🔴 没有有效的PCM数据');
          return;
        }
        
        console.log('🎵 总PCM数据长度:', allPcmData.length, '个采样点');
        console.log('🎵 预计播放时长:', (allPcmData.length / 24000).toFixed(2), '秒');
        
        // 转换为WAV并播放
        const wavBlob = pcmToWav(new Int16Array(allPcmData), 24000);
        console.log('🎵 WAV文件大小:', wavBlob.size, 'bytes');
        
        const audioUrl = URL.createObjectURL(wavBlob);
        const audio = new Audio(audioUrl);
        
        // 设置音量
        audio.volume = 1.0;
        
        audio.onloadedmetadata = () => {
          console.log('🎵 音频元数据加载完成，时长:', audio.duration, '秒');
        };
        
        audio.oncanplay = () => {
          console.log('🎵 音频可以播放了');
        };
        
        audio.onplay = () => {
          console.log('🎵 音频开始播放');
        };
        
        audio.onended = () => {
          console.log('🎵 音频播放完成');
          URL.revokeObjectURL(audioUrl);
        };
        
        audio.onerror = (error) => {
          console.error('🔴 音频播放错误:', error);
          console.error('🔴 错误代码:', audio.error?.code);
          console.error('🔴 错误消息:', audio.error?.message);
        };
        
        try {
          await audio.play();
          console.log('✅ 音频播放命令已发送');
        } catch (playError) {
          console.error('🔴 播放失败:', playError);
        }
        
      } catch (error) {
        console.error('🔴 播放音频过程出错:', error);
        console.error('🔴 错误堆栈:', error.stack);
      } finally {
        // 清空音频缓冲
        audioChunks.value = [];
      }
    };
    
    // PCM转WAV（在组件内部实现）
    const pcmToWav = (pcmData, sampleRate = 24000) => {
      const numChannels = 1;
      const bitsPerSample = 16;
      const byteRate = sampleRate * numChannels * bitsPerSample / 8;
      const blockAlign = numChannels * bitsPerSample / 8;
      const dataSize = pcmData.length * 2;

      const buffer = new ArrayBuffer(44 + dataSize);
      const view = new DataView(buffer);

      // WAV文件头
      const writeString = (offset, string) => {
        for (let i = 0; i < string.length; i++) {
          view.setUint8(offset + i, string.charCodeAt(i));
        }
      };

      writeString(0, 'RIFF');
      view.setUint32(4, 36 + dataSize, true);
      writeString(8, 'WAVE');
      writeString(12, 'fmt ');
      view.setUint32(16, 16, true);
      view.setUint16(20, 1, true);
      view.setUint16(22, numChannels, true);
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, byteRate, true);
      view.setUint16(32, blockAlign, true);
      view.setUint16(34, bitsPerSample, true);
      writeString(36, 'data');
      view.setUint32(40, dataSize, true);

      // 写入PCM数据
      for (let i = 0; i < pcmData.length; i++) {
        view.setInt16(44 + i * 2, pcmData[i], true);
      }

      return new Blob([buffer], { type: 'audio/wav' });
    };

    // 断开连接
    const disconnectWebSocket = () => {
      if (isRecording.value) {
        stopRecording();
      }

      if (wsService.value) {
        wsService.value.close();
        wsService.value = null;
      }

      isConnected.value = false;
      connectionStatus.value = 'disconnected';
      stopDurationTimer();
    };

    // 切换连接状态
    const toggleConnection = () => {
      if (isConnected.value) {
        disconnectWebSocket();
      } else {
        connectWebSocket();
      }
    };

    // 开始录音
    const startRecording = () => {
      if (!isConnected.value || !webrtcService.value) {
        alert('请先建立连接');
        return;
      }

      let audioSentCount = 0;
      webrtcService.value.startRecording((audioData) => {
        // 发送音频数据到服务器
        if (wsService.value && wsService.value.isConnected()) {
          audioSentCount++;
          if (audioSentCount === 1 || audioSentCount % 50 === 0) {
            console.log(`🎤 已发送 ${audioSentCount} 个音频包，最新大小: ${audioData.data.length} bytes`);
          }
          wsService.value.send({
            type: 'input_audio_buffer.append',
            audio: audioData.data // PCM base64数据，不需要split
          });
        } else {
          console.warn('⚠️ WebSocket未连接，无法发送音频');
        }
      });

      isRecording.value = true;
      console.log('✅ 开始录音，准备发送音频数据...');
    };

    // 停止录音
    const stopRecording = () => {
      if (webrtcService.value) {
        webrtcService.value.stopRecording();
      }

      // 通知服务器提交音频
      if (wsService.value && wsService.value.isConnected()) {
        wsService.value.send({
          type: 'input_audio_buffer.commit'
        });

        // 请求生成响应
        wsService.value.send({
          type: 'response.create'
        });
      }

      isRecording.value = false;
    };

    // 切换录音状态
    const toggleRecording = () => {
      if (isRecording.value) {
        stopRecording();
      } else {
        startRecording();
      }
    };

    // 切换静音
    const toggleMute = () => {
      isMuted.value = !isMuted.value;
      // 这里可以实现静音逻辑
      if (isMuted.value) {
        // 静音输出
        console.log('已静音');
      } else {
        // 取消静音
        console.log('取消静音');
      }
    };

    // 通话时长计时器
    let durationTimer = null;
    const startDurationTimer = () => {
      durationTimer = setInterval(() => {
        if (callStartTime.value) {
          callDuration.value = Math.floor((Date.now() - callStartTime.value) / 1000);
        }
      }, 1000);
    };

    const stopDurationTimer = () => {
      if (durationTimer) {
        clearInterval(durationTimer);
        durationTimer = null;
      }
      callDuration.value = 0;
      callStartTime.value = null;
    };

    // 返回
    const goBack = () => {
      if (isConnected.value) {
        if (confirm('通话进行中，确定要退出吗？')) {
          disconnectWebSocket();
          router.back();
        }
      } else {
        router.back();
      }
    };

    // 生命周期
    onMounted(() => {
      initializeServices();
    });

    onBeforeUnmount(() => {
      // 清理资源
      if (isRecording.value) {
        stopRecording();
      }
      
      if (wsService.value) {
        wsService.value.close();
      }

      if (webrtcService.value) {
        webrtcService.value.cleanup();
      }

      stopDurationTimer();
    });

    return {
      // 状态
      isConnected,
      isConnecting,
      connectionStatus,
      isRecording,
      isMuted,
      isSpeaking,
      volumeLevel,
      sampleRate,
      callDuration,
      transcript,
      showDebug,

      // 计算属性
      statusText,
      formattedDuration,
      debugInfo,

      // 方法
      toggleConnection,
      toggleRecording,
      toggleMute,
      goBack
    };
  }
};
</script>

<style scoped>
.voice-call-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  overflow: hidden;
}

/* 顶部导航栏 */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.back-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 0.875rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #fff;
}

.status-indicator.connected .status-dot {
  background: #4ade80;
  box-shadow: 0 0 10px #4ade80;
  animation: pulse 2s infinite;
}

.status-indicator.connecting .status-dot,
.status-indicator.reconnecting .status-dot {
  background: #fbbf24;
  animation: blink 1s infinite;
}

.status-indicator.error .status-dot {
  background: #ef4444;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes blink {
  0%, 50%, 100% { opacity: 1; }
  25%, 75% { opacity: 0.3; }
}

/* 主内容区域 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  overflow-y: auto;
  gap: 2rem;
}

/* 音频可视化 */
.audio-visualizer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
}

.avatar-container {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  z-index: 2;
}

.avatar.active {
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
}

.wave-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: wave 2s infinite;
  z-index: 1;
}

.wave-ring-2 {
  animation-delay: 0.3s;
}

.wave-ring-3 {
  animation-delay: 0.6s;
}

@keyframes wave {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.8);
    opacity: 0;
  }
}

/* 音量指示器 */
.volume-indicator {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.volume-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.volume-fill {
  height: 100%;
  background: linear-gradient(90deg, #4ade80, #22c55e);
  transition: width 0.1s;
  border-radius: 4px;
}

.volume-text {
  text-align: center;
  font-size: 0.875rem;
  opacity: 0.8;
}

/* 对话信息 */
.conversation-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  opacity: 0.8;
}

.info-value {
  font-weight: 600;
}

.info-value.connected {
  color: #4ade80;
}

.info-value.error {
  color: #ef4444;
}

/* 转录文本 */
.transcript-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-height: 300px;
  overflow-y: auto;
}

.transcript-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.transcript-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.transcript-item {
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: flex;
  gap: 0.5rem;
}

.transcript-item.user {
  background: rgba(102, 126, 234, 0.3);
}

.transcript-item.assistant {
  background: rgba(118, 75, 162, 0.3);
}

.speaker {
  font-weight: 600;
  min-width: 40px;
}

/* 控制按钮 */
.controls {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  padding: 2rem 0;
  flex-wrap: wrap;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
  font-weight: 500;
  min-width: 120px;
}

.control-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.record-btn {
  min-width: 150px;
  background: rgba(239, 68, 68, 0.3);
}

.record-btn.active {
  background: rgba(239, 68, 68, 0.6);
  border-color: #ef4444;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
}

.connect-btn {
  background: rgba(34, 197, 94, 0.3);
}

.connect-btn:hover:not(:disabled) {
  background: rgba(34, 197, 94, 0.5);
}

/* 调试面板 */
.debug-panel {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  padding: 1rem;
  margin-top: auto;
}

.debug-panel h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
}

.debug-panel pre {
  margin: 0;
  font-size: 0.75rem;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }

  .controls {
    gap: 1rem;
  }

  .control-btn {
    min-width: 100px;
    padding: 1rem;
  }

  .avatar-container {
    width: 150px;
    height: 150px;
  }

  .avatar {
    width: 100px;
    height: 100px;
  }

  .wave-ring {
    width: 100px;
    height: 100px;
  }
}
</style>

