/**
 * WebSocket连接服务
 * 负责与后端建立和维护长连接
 */

class WebSocketService {
  constructor() {
    this.ws = null;
    this.url = '';
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
    this.isIntentionallyClosed = false;
    this.messageHandlers = new Map();
    this.connectionStateListeners = [];
    this.heartbeatInterval = null;
    this.heartbeatTimeout = null;
  }

  /**
   * 连接到WebSocket服务器
   */
  connect(url, protocols = []) {
    return new Promise((resolve, reject) => {
      try {
        this.url = url;
        this.isIntentionallyClosed = false;

        // 创建WebSocket连接
        this.ws = new WebSocket(url, protocols);

        // 连接打开
        this.ws.onopen = () => {
          console.log('WebSocket连接已建立');
          this.reconnectAttempts = 0;
          this.notifyConnectionStateChange('connected');
          this.startHeartbeat();
          resolve();
        };

        // 接收消息
        this.ws.onmessage = (event) => {
          // const preview = typeof event.data === 'string' ? event.data.substring(0, 100) : 'binary';
          // console.log('📥 收到服务器消息:', preview + '...');  // 注释掉避免刷屏
          this.handleMessage(event);
        };

        // 连接关闭
        this.ws.onclose = (event) => {
          console.log('WebSocket连接已关闭', event.code, event.reason);
          this.notifyConnectionStateChange('disconnected');
          this.stopHeartbeat();

          // 如果不是主动关闭，尝试重连
          if (!this.isIntentionallyClosed && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.attemptReconnect();
          }
        };

        // 连接错误
        this.ws.onerror = (error) => {
          console.error('WebSocket错误:', error);
          this.notifyConnectionStateChange('error');
          reject(error);
        };

      } catch (error) {
        console.error('创建WebSocket连接失败:', error);
        reject(error);
      }
    });
  }

  /**
   * 处理接收到的消息
   */
  handleMessage(event) {
    try {
      let message;
      
      // 处理文本消息
      if (typeof event.data === 'string') {
        try {
          message = JSON.parse(event.data);
          console.log('📨 收到消息类型:', message.type);
        } catch {
          message = { type: 'text', data: event.data };
        }
      } 
      // 处理二进制消息
      else if (event.data instanceof Blob) {
        this.handleBinaryMessage(event.data);
        return;
      } 
      // 处理ArrayBuffer
      else if (event.data instanceof ArrayBuffer) {
        message = { type: 'binary', data: event.data };
      }

      // 调用对应类型的消息处理器
      if (message && message.type) {
        const handler = this.messageHandlers.get(message.type);
        if (handler) {
          console.log('✅ 调用处理器:', message.type);
          handler(message);
        } else {
          console.warn('⚠️ 没有找到处理器:', message.type);
        }

        // 同时调用通用消息处理器
        const genericHandler = this.messageHandlers.get('*');
        if (genericHandler) {
          genericHandler(message);
        }
      }

    } catch (error) {
      console.error('处理消息失败:', error);
    }
  }

  /**
   * 处理二进制消息
   */
  async handleBinaryMessage(blob) {
    try {
      const arrayBuffer = await blob.arrayBuffer();
      const message = {
        type: 'binary',
        data: arrayBuffer,
        blob: blob
      };

      const handler = this.messageHandlers.get('binary');
      if (handler) {
        handler(message);
      }
    } catch (error) {
      console.error('处理二进制消息失败:', error);
    }
  }

  /**
   * 发送消息
   */
  send(message) {
    if (!this.isConnected()) {
      console.error('WebSocket未连接');
      return false;
    }

    try {
      if (typeof message === 'object') {
        this.ws.send(JSON.stringify(message));
      } else {
        this.ws.send(message);
      }
      return true;
    } catch (error) {
      console.error('发送消息失败:', error);
      return false;
    }
  }

  /**
   * 发送二进制数据
   */
  sendBinary(data) {
    if (!this.isConnected()) {
      console.error('WebSocket未连接');
      return false;
    }

    try {
      this.ws.send(data);
      return true;
    } catch (error) {
      console.error('发送二进制数据失败:', error);
      return false;
    }
  }

  /**
   * 注册消息处理器
   * @param {string} type - 消息类型，使用'*'可以监听所有消息
   * @param {function} handler - 处理函数
   */
  on(type, handler) {
    this.messageHandlers.set(type, handler);
  }

  /**
   * 移除消息处理器
   */
  off(type) {
    this.messageHandlers.delete(type);
  }

  /**
   * 监听连接状态变化
   */
  onConnectionStateChange(listener) {
    this.connectionStateListeners.push(listener);
  }

  /**
   * 通知连接状态变化
   */
  notifyConnectionStateChange(state) {
    this.connectionStateListeners.forEach(listener => {
      try {
        listener(state);
      } catch (error) {
        console.error('连接状态监听器错误:', error);
      }
    });
  }

  /**
   * 尝试重新连接
   */
  attemptReconnect() {
    this.reconnectAttempts++;
    const delay = this.reconnectDelay * this.reconnectAttempts;

    console.log(`${delay}ms后尝试第${this.reconnectAttempts}次重连...`);
    this.notifyConnectionStateChange('reconnecting');

    setTimeout(() => {
      if (!this.isIntentionallyClosed) {
        this.connect(this.url).catch(error => {
          console.error('重连失败:', error);
        });
      }
    }, delay);
  }

  /**
   * 启动心跳检测
   */
  startHeartbeat(interval = 30000) {
    this.stopHeartbeat();

    this.heartbeatInterval = setInterval(() => {
      if (this.isConnected()) {
        this.send({ type: 'ping' });

        // 设置心跳超时检测
        this.heartbeatTimeout = setTimeout(() => {
          console.warn('心跳超时，重新连接...');
          this.ws.close();
        }, 10000);
      }
    }, interval);

    // 监听pong消息
    this.on('pong', () => {
      if (this.heartbeatTimeout) {
        clearTimeout(this.heartbeatTimeout);
        this.heartbeatTimeout = null;
      }
    });
  }

  /**
   * 停止心跳检测
   */
  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
    if (this.heartbeatTimeout) {
      clearTimeout(this.heartbeatTimeout);
      this.heartbeatTimeout = null;
    }
  }

  /**
   * 检查连接状态
   */
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }

  /**
   * 获取连接状态
   */
  getReadyState() {
    if (!this.ws) return 'CLOSED';
    
    const states = {
      [WebSocket.CONNECTING]: 'CONNECTING',
      [WebSocket.OPEN]: 'OPEN',
      [WebSocket.CLOSING]: 'CLOSING',
      [WebSocket.CLOSED]: 'CLOSED'
    };
    
    return states[this.ws.readyState] || 'UNKNOWN';
  }

  /**
   * 关闭连接
   */
  close(code = 1000, reason = 'Normal closure') {
    this.isIntentionallyClosed = true;
    this.stopHeartbeat();

    if (this.ws) {
      try {
        this.ws.close(code, reason);
      } catch (error) {
        console.error('关闭WebSocket连接失败:', error);
      }
    }

    this.ws = null;
    this.messageHandlers.clear();
    this.connectionStateListeners = [];
  }
}

export default WebSocketService;

