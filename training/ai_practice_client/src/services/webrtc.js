/**
 * WebRTC音频服务
 * 负责音频捕获、处理和编码
 */

class WebRTCService {
  constructor() {
    this.audioContext = null;
    this.mediaStream = null;
    this.mediaRecorder = null;
    this.audioWorkletNode = null;
    this.analyser = null;
    this.isRecording = false;
    this.onAudioDataCallback = null;
    this.onVolumeChangeCallback = null;
  }

  /**
   * 初始化音频上下文和获取麦克风权限
   */
  async initialize() {
    try {
      // 创建音频上下文
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 24000, // realtime API 支持的采样率
        latencyHint: 'interactive'
      });

      // 请求麦克风权限
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true, // 回声消除
          noiseSuppression: true, // 噪音抑制
          autoGainControl: true,  // 自动增益控制
          channelCount: 1,        // 单声道
          sampleRate: 24000
        },
        video: false
      });

      // 创建音频分析器（用于音量可视化）
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      this.analyser.smoothingTimeConstant = 0.8;

      // 连接音频流到分析器
      const source = this.audioContext.createMediaStreamSource(this.mediaStream);
      source.connect(this.analyser);

      console.log('WebRTC音频服务初始化成功');
      return true;
    } catch (error) {
      console.error('初始化音频失败:', error);
      throw new Error('无法访问麦克风，请检查权限设置');
    }
  }

  /**
   * 开始录音并实时发送音频数据
   */
  startRecording(onAudioData) {
    if (this.isRecording) {
      console.warn('已在录音中');
      return;
    }

    this.onAudioDataCallback = onAudioData;
    this.isRecording = true;

    // 使用AudioWorklet或ScriptProcessorNode获取PCM数据
    this.startPCMRecording();

    // 启动音量监控
    this.startVolumeMonitoring();
  }

  /**
   * 开始PCM录音（用于DashScope）
   */
  startPCMRecording() {
    try {
      const source = this.audioContext.createMediaStreamSource(this.mediaStream);
      
      // 使用ScriptProcessorNode处理音频（兼容性更好）
      const bufferSize = 2048;
      const processor = this.audioContext.createScriptProcessor(bufferSize, 1, 1);
      
      processor.onaudioprocess = (e) => {
        if (!this.isRecording) return;
        
        const inputData = e.inputBuffer.getChannelData(0);
        
        // 将Float32转换为Int16 PCM
        const pcm16 = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          const s = Math.max(-1, Math.min(1, inputData[i]));
          pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }
        
        // 转换为Base64
        const base64 = this.arrayBufferToBase64(pcm16.buffer);
        
        if (this.onAudioDataCallback) {
          this.onAudioDataCallback({
            type: 'audio',
            data: base64,
            format: 'pcm16',
            sampleRate: this.audioContext.sampleRate
          });
        }
      };
      
      source.connect(processor);
      processor.connect(this.audioContext.destination);
      
      // 保存引用以便后续清理
      this.audioProcessor = processor;
      this.audioSource = source;
      
      console.log('开始PCM录音, 采样率:', this.audioContext.sampleRate);
      
    } catch (error) {
      console.error('启动PCM录音失败:', error);
      this.isRecording = false;
    }
  }

  /**
   * ArrayBuffer转Base64
   */
  arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  /**
   * 停止录音
   */
  stopRecording() {
    if (this.isRecording) {
      this.isRecording = false;
      this.stopVolumeMonitoring();
      
      // 清理AudioProcessor
      if (this.audioProcessor) {
        this.audioProcessor.disconnect();
        this.audioProcessor = null;
      }
      
      if (this.audioSource) {
        this.audioSource.disconnect();
        this.audioSource = null;
      }
      
      console.log('停止录音');
    }
  }

  /**
   * 开始音量监控
   */
  startVolumeMonitoring() {
    if (!this.analyser) return;

    const bufferLength = this.analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const updateVolume = () => {
      if (!this.isRecording) return;

      this.analyser.getByteFrequencyData(dataArray);
      
      // 计算平均音量
      let sum = 0;
      for (let i = 0; i < bufferLength; i++) {
        sum += dataArray[i];
      }
      const average = sum / bufferLength;
      const volume = Math.min(100, (average / 255) * 100);

      if (this.onVolumeChangeCallback) {
        this.onVolumeChangeCallback(volume);
      }

      requestAnimationFrame(updateVolume);
    };

    updateVolume();
  }

  /**
   * 停止音量监控
   */
  stopVolumeMonitoring() {
    // 音量监控会在 isRecording 为 false 时自动停止
  }

  /**
   * 设置音量变化回调
   */
  onVolumeChange(callback) {
    this.onVolumeChangeCallback = callback;
  }

  /**
   * 播放接收到的音频数据
   */
  async playAudio(audioData, format = 'base64') {
    try {
      let audioBlob;
      
      if (format === 'base64') {
        // 将Base64转换为Blob
        const binaryString = atob(audioData.split(',')[1] || audioData);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        audioBlob = new Blob([bytes], { type: 'audio/webm' });
      } else if (format === 'pcm') {
        // 处理PCM格式音频
        audioBlob = await this.pcmToWav(audioData);
      } else {
        audioBlob = audioData;
      }

      // 创建音频元素并播放
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);
      };

      await audio.play();
    } catch (error) {
      console.error('播放音频失败:', error);
    }
  }

  /**
   * PCM转WAV格式
   */
  async pcmToWav(pcmData, sampleRate = 24000) {
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
    const pcmArray = new Int16Array(pcmData);
    for (let i = 0; i < pcmArray.length; i++) {
      view.setInt16(44 + i * 2, pcmArray[i], true);
    }

    return new Blob([buffer], { type: 'audio/wav' });
  }

  /**
   * Blob转Base64
   */
  convertBlobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  /**
   * 获取支持的音频格式
   */
  getSupportedMimeType() {
    const types = [
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/ogg;codecs=opus',
      'audio/mp4'
    ];

    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        return type;
      }
    }

    return 'audio/webm'; // 默认返回
  }

  /**
   * 暂停音频上下文（节省资源）
   */
  async suspend() {
    if (this.audioContext && this.audioContext.state === 'running') {
      await this.audioContext.suspend();
    }
  }

  /**
   * 恢复音频上下文
   */
  async resume() {
    if (this.audioContext && this.audioContext.state === 'suspended') {
      await this.audioContext.resume();
    }
  }

  /**
   * 清理资源
   */
  cleanup() {
    this.stopRecording();

    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
      this.mediaStream = null;
    }

    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }

    this.analyser = null;
    this.mediaRecorder = null;
    this.audioProcessor = null;
    this.audioSource = null;
    this.onAudioDataCallback = null;
    this.onVolumeChangeCallback = null;
  }

  /**
   * 获取当前音频状态
   */
  getStatus() {
    return {
      isRecording: this.isRecording,
      audioContextState: this.audioContext?.state,
      hasMediaStream: !!this.mediaStream,
      sampleRate: this.audioContext?.sampleRate
    };
  }
}

export default WebRTCService;

