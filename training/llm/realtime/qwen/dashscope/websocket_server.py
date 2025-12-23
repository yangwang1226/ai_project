"""
WebSocket服务器 - 包装DashScope Realtime API
"""
import os
import sys
import json
import base64
import asyncio
import logging
from typing import Dict, Optional
import websockets
from websockets.server import WebSocketServerProtocol
import dashscope
from dashscope.audio.qwen_omni import *

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 服务器配置
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# 音频格式配置
INPUT_AUDIO_FORMAT = AudioFormat.PCM_24000HZ_MONO_16BIT  # 前端使用24kHz
OUTPUT_AUDIO_FORMAT = AudioFormat.PCM_24000HZ_MONO_16BIT

# 默认提示词文件路径
DEFAULT_PROMPT_FILE = './llm/realtime/qwen/dashscope/prompts/sales_training.txt'


def init_dashscope_api_key():
    """初始化DashScope API密钥"""
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
        logger.info('API Key loaded from environment variable')
    else:
        dashscope.api_key = 'sk-8e0b5b24b5874bc5a7af77dae8e846d4'
        logger.warning('Using hardcoded API Key')


def load_prompt(prompt_file: str = DEFAULT_PROMPT_FILE) -> str:
    """加载提示词文件"""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f'Prompt loaded from {prompt_file}')
            return content
    except FileNotFoundError:
        logger.error(f'Prompt file not found: {prompt_file}')
        return "你是一个友好的AI助手。"
    except Exception as e:
        logger.error(f'Error loading prompt: {e}')
        return "你是一个友好的AI助手。"


class RealtimeCallback(OmniRealtimeCallback):
    """Realtime API回调处理"""
    
    def __init__(self, websocket: WebSocketServerProtocol, session_id: str):
        self.websocket = websocket
        self.session_id = session_id
        self.is_closed = False
    
    def on_open(self) -> None:
        logger.info(f'[{self.session_id}] DashScope connection opened')
    
    def on_close(self, close_status_code, close_msg) -> None:
        logger.info(f'[{self.session_id}] DashScope connection closed: {close_status_code} - {close_msg}')
        self.is_closed = True
    
    def on_event(self, response: dict) -> None:
        """处理DashScope事件并转发给前端"""
        try:
            event_type = response.get('type', '')
            
            # 会话创建
            if event_type == 'session.created':
                logger.info(f'[{self.session_id}] Session created')
                asyncio.create_task(self.send_to_client({
                    'type': 'session.created',
                    'session': {
                        'id': response.get('session', {}).get('id', self.session_id),
                        'model': 'qwen3-omni-flash-realtime',
                        'created_at': response.get('session', {}).get('created_at', 0)
                    }
                }))
            
            # 会话更新
            elif event_type == 'session.updated':
                logger.info(f'[{self.session_id}] Session updated')
                asyncio.create_task(self.send_to_client({
                    'type': 'session.updated',
                    'session': response.get('session', {})
                }))
            
            # 会话错误
            elif event_type == 'session.error':
                logger.error(f'[{self.session_id}] Session error: {response}')
                asyncio.create_task(self.send_to_client({
                    'type': 'error',
                    'error': {
                        'code': 'session_error',
                        'message': response.get('session', {}).get('error', 'Unknown error')
                    }
                }))
            
            # 用户输入转录完成
            elif event_type == 'conversation.item.input_audio_transcription.completed':
                transcript = response.get('transcript', '')
                logger.info(f'[{self.session_id}] User said: {transcript}')
                asyncio.create_task(self.send_to_client({
                    'type': 'conversation.item.created',
                    'item': {
                        'id': response.get('item_id', ''),
                        'role': 'user',
                        'content': [{
                            'type': 'text',
                            'transcript': transcript
                        }]
                    }
                }))
            
            # AI响应文本增量
            elif event_type == 'response.audio_transcript.delta':
                text_delta = response.get('delta', '')
                logger.debug(f'[{self.session_id}] AI text delta: {text_delta}')
                asyncio.create_task(self.send_to_client({
                    'type': 'response.text.delta',
                    'delta': text_delta,
                    'response_id': response.get('response_id', '')
                }))
            
            # AI响应音频增量
            elif event_type == 'response.audio.delta':
                audio_delta = response.get('delta', '')
                asyncio.create_task(self.send_to_client({
                    'type': 'response.audio.delta',
                    'delta': audio_delta,
                    'response_id': response.get('response_id', '')
                }))
            
            # 语音活动检测 - 用户开始说话
            elif event_type == 'input_audio_buffer.speech_started':
                logger.info(f'[{self.session_id}] VAD: Speech started')
                asyncio.create_task(self.send_to_client({
                    'type': 'input_audio_buffer.speech_started'
                }))
            
            # 语音活动检测 - 用户停止说话
            elif event_type == 'input_audio_buffer.speech_stopped':
                logger.info(f'[{self.session_id}] VAD: Speech stopped')
                asyncio.create_task(self.send_to_client({
                    'type': 'input_audio_buffer.speech_stopped'
                }))
            
            # 响应完成
            elif event_type == 'response.done':
                logger.info(f'[{self.session_id}] Response done')
                asyncio.create_task(self.send_to_client({
                    'type': 'response.audio.done',
                    'response_id': response.get('response_id', '')
                }))
                
                # 如果有完整的转录文本，也发送
                if 'output' in response:
                    for output_item in response['output']:
                        if output_item.get('type') == 'message':
                            content = output_item.get('content', [])
                            for item in content:
                                if item.get('type') == 'text':
                                    asyncio.create_task(self.send_to_client({
                                        'type': 'conversation.item.created',
                                        'item': {
                                            'id': output_item.get('id', ''),
                                            'role': 'assistant',
                                            'content': [{
                                                'type': 'text',
                                                'transcript': item.get('text', '')
                                            }]
                                        }
                                    }))
            
        except Exception as e:
            logger.error(f'[{self.session_id}] Error in on_event: {e}', exc_info=True)
    
    async def send_to_client(self, message: dict):
        """发送消息给前端客户端"""
        try:
            if not self.is_closed:
                await self.websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f'[{self.session_id}] Error sending to client: {e}')


class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        self.sessions: Dict[str, OmniRealtimeConversation] = {}
        self.callbacks: Dict[str, RealtimeCallback] = {}
    
    def create_session(
        self, 
        session_id: str, 
        websocket: WebSocketServerProtocol,
        voice: str = 'Cherry',
        instructions: str = None
    ) -> OmniRealtimeConversation:
        """创建新会话"""
        try:
            # 创建回调
            callback = RealtimeCallback(websocket, session_id)
            self.callbacks[session_id] = callback
            
            # 创建会话
            conversation = OmniRealtimeConversation(
                model='qwen3-omni-flash-realtime',
                callback=callback
            )
            
            # 连接
            conversation.connect()
            
            # 更新会话配置
            if instructions is None:
                instructions = load_prompt()
            
            conversation.update_session(
                output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
                voice=voice,
                input_audio_format=INPUT_AUDIO_FORMAT,
                output_audio_format=OUTPUT_AUDIO_FORMAT,
                enable_input_audio_transcription=True,
                input_audio_transcription_model='gummy-realtime-v1',
                enable_turn_detection=True,
                turn_detection_type='server_vad',
                instructions=instructions
            )
            
            self.sessions[session_id] = conversation
            logger.info(f'[{session_id}] Session created with voice: {voice}')
            
            return conversation
            
        except Exception as e:
            logger.error(f'[{session_id}] Error creating session: {e}', exc_info=True)
            raise
    
    def get_session(self, session_id: str) -> Optional[OmniRealtimeConversation]:
        """获取会话"""
        return self.sessions.get(session_id)
    
    def close_session(self, session_id: str):
        """关闭会话"""
        if session_id in self.sessions:
            try:
                self.sessions[session_id].close()
            except Exception as e:
                logger.error(f'[{session_id}] Error closing session: {e}')
            
            del self.sessions[session_id]
            if session_id in self.callbacks:
                del self.callbacks[session_id]
            
            logger.info(f'[{session_id}] Session closed')


# 全局会话管理器
session_manager = SessionManager()


async def handle_client(websocket: WebSocketServerProtocol, path: str):
    """处理客户端连接"""
    session_id = f"session_{id(websocket)}"
    conversation = None
    
    logger.info(f'[{session_id}] Client connected from {websocket.remote_address}')
    
    try:
        async for message in websocket:
            try:
                # 解析消息
                data = json.loads(message)
                msg_type = data.get('type', '')
                
                logger.debug(f'[{session_id}] Received: {msg_type}')
                
                # 创建会话
                if msg_type == 'session.create':
                    session_config = data.get('session', {})
                    voice = session_config.get('voice', 'Cherry')
                    instructions = session_config.get('instructions')
                    
                    conversation = session_manager.create_session(
                        session_id, 
                        websocket,
                        voice=voice,
                        instructions=instructions
                    )
                
                # 追加音频数据
                elif msg_type == 'input_audio_buffer.append':
                    if conversation:
                        audio_b64 = data.get('audio', '')
                        # DashScope期望直接的base64字符串，不需要data URI前缀
                        if ',' in audio_b64:
                            audio_b64 = audio_b64.split(',', 1)[1]
                        conversation.append_audio(audio_b64)
                    else:
                        await websocket.send(json.dumps({
                            'type': 'error',
                            'error': {
                                'code': 'session_not_found',
                                'message': 'Session not created. Send session.create first.'
                            }
                        }))
                
                # 提交音频（DashScope会自动处理VAD，这个消息可以忽略）
                elif msg_type == 'input_audio_buffer.commit':
                    logger.debug(f'[{session_id}] Audio buffer commit (handled by VAD)')
                
                # 创建响应（DashScope会自动响应，这个消息可以忽略）
                elif msg_type == 'response.create':
                    logger.debug(f'[{session_id}] Response create (handled automatically)')
                
                # 心跳
                elif msg_type == 'ping':
                    await websocket.send(json.dumps({'type': 'pong'}))
                
                # 取消响应
                elif msg_type == 'response.cancel':
                    logger.info(f'[{session_id}] Response cancel requested')
                    # DashScope API可能不支持取消，这里只是记录
                
                # 未知消息类型
                else:
                    logger.warning(f'[{session_id}] Unknown message type: {msg_type}')
                
            except json.JSONDecodeError as e:
                logger.error(f'[{session_id}] JSON decode error: {e}')
                await websocket.send(json.dumps({
                    'type': 'error',
                    'error': {
                        'code': 'invalid_json',
                        'message': str(e)
                    }
                }))
            except Exception as e:
                logger.error(f'[{session_id}] Error handling message: {e}', exc_info=True)
                await websocket.send(json.dumps({
                    'type': 'error',
                    'error': {
                        'code': 'internal_error',
                        'message': str(e)
                    }
                }))
    
    except websockets.exceptions.ConnectionClosed:
        logger.info(f'[{session_id}] Client disconnected')
    except Exception as e:
        logger.error(f'[{session_id}] Connection error: {e}', exc_info=True)
    finally:
        # 清理会话
        session_manager.close_session(session_id)


async def main():
    """启动WebSocket服务器"""
    init_dashscope_api_key()
    
    logger.info(f'Starting WebSocket server on {SERVER_HOST}:{SERVER_PORT}')
    logger.info(f'WebSocket endpoint: ws://{SERVER_HOST}:{SERVER_PORT}/ws/realtime')
    
    async with websockets.serve(
        handle_client,
        SERVER_HOST,
        SERVER_PORT,
        subprotocols=['realtime'],
        ping_interval=30,
        ping_timeout=10
    ):
        logger.info('WebSocket server started successfully')
        await asyncio.Future()  # 永久运行


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Server stopped by user')
    except Exception as e:
        logger.error(f'Server error: {e}', exc_info=True)
        sys.exit(1)

