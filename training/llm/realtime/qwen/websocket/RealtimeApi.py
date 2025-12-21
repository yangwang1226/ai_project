import json
import asyncio
import os
from datetime import datetime, timezone
import websockets
from dotenv import load_dotenv
from websockets import ConnectionClosedError
from realtime.gpt.RealtimeEventHandler import RealtimeEventHandler
import logging
logging.basicConfig(level=logging.INFO)

# 获取环境变量 ENV 的值，默认为 'dev'
env_suffix = os.getenv('ENV', 'prod')
# 构造环境变量文件路径
env_file = os.path.join(os.path.dirname(__file__), "..", "env", f".env.{env_suffix}")
# 加载环境变量文件
load_dotenv(env_file)

# 生成id
def _generate_id(prefix):
    return f"{prefix}{int(datetime.now(timezone.utc).timestamp() * 1000)}"


class StepFunApi(RealtimeEventHandler):
    #初始化接口
    def __init__(self):
        super().__init__()
        # 获取环境变量中的主机地址
        self.host = os.getenv('STEP_URL', 'wss://api.stepfun.com/v1/realtime')
        # 获取环境变量中的密钥
        self.STEP_API_KEY = os.getenv('STEP_API_KEY')
        # 获取环境变量中的模型名称
        self.model = os.getenv('STEP_MODEL')
        # 初始化的模型链接
        self.ws = None

    #判断是否连接
    def is_connected(self):
        return self.ws is not None

    #与服务器建立连接
    async def connect(self, host=None, key=None, model='step-audio-2'):
        if self.is_connected():
            logging.info("阶跃星辰realtime长链接已连接……")
            return
        key = key or self.STEP_API_KEY
        host = host or self.host
        model = model or self.model
        logging.info(f"正在连接到 {host}")
        conn = await asyncio.wait_for(
            websockets.connect(
                f"{host}?model={model}",
                additional_headers={"Authorization": f"Bearer {key}"},
                ping_interval=1,
                max_size=20 * 2 ** 20,
                max_queue=1024,
                write_limit=2 ** 20
            ),
            timeout=10)
        self.ws = conn
        asyncio.create_task(self._receive_messages())

    #断开连接
    async def disconnect(self):
        if self.ws:
            await self.ws.close()
            self.ws = None
            logging.info(f"已与阶跃星辰服务器断开连接……")

    #接收消息
    async def _receive_messages(self):
        logging.info("开始监听消息...")
        try:
            async for message in self.ws:
                event = json.loads(message)
                # logging.info(f"接收到模型消息原文: {event}")
                self.dispatch(f"server.{event['type']}", event)
        except ConnectionClosedError as e:
            logging.error(f"接收模型资源服务连接异常, {e}", exc_info=True)

    #发送消息
    async def send(self, event_name, data=None):
        data = data or {}
        event = {
            "event_id": _generate_id("evt_"),
            "type": event_name,
            **data
        }
        self.dispatch(f"client.{event_name}", event)
        self.dispatch("client.*", event)
        try:
            await self.ws.send(json.dumps(event))
        except Exception as e:
            logging.error(f"发送模型资源服务异常, {e}", exc_info=True)

if __name__ == '__main__':
    api = StepFunApi()
    asyncio.run(api.connect('wss://api.stepfun.com/v1/realtime',
                '638O3OyvOs5Sjc8zL1R8sLIHtaMXhDyP0jEZbUIhGNDRbSsTqVJxBKmfBuaw7WCZS'))
