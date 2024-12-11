import asyncio
from typing import Any
import websockets
import json
from eve.emotions.emotion import Emotion
from eve_lib.llms import Ollama, ZhiPuAI
from eve_lib.memory import ConversationBufferMemory
from eve_lib.chains import LLMChain
from eve_lib.output_parsers import RegexParser
from eve.prompts.prompt import PROMPT

llm = ZhiPuAI()
memory = ConversationBufferMemory(human_prefix="Jin", ai_prefix="eve")
chat_chain = LLMChain(memory=memory, prompt=PROMPT, llm=llm)
parser = RegexParser(regex=r"(.*?)（(.*?)）：(.*)", output_keys=["name", "mode", "content"], default_output_key="content")
emotion = Emotion.from_llm(llm=llm)
async def chat_handler(websocket: Any) -> None:
    try:
        async for message in websocket:
            data = json.loads(message)
            input = data.get("query", "")
            if input == "clear":
                memory.clear()
                await websocket.send(json.dumps({"response": "记忆已被清空"}))
                continue
            if not input:
                await websocket.send(json.dumps({"error": "问题不能为空"}))
            emotion.update_emotional_state(input)
            print(str(emotion.historical_emotions))
            output = chat_chain.run(input=input, emotion_state=emotion.format_emotion_state())
            res = parser.parse(output)
            response = f"{res['content']}"
            print(response)
            await websocket.send(json.dumps({"response":response}))
    except websockets.ConnectionClosed as e:
        raise ValueError(f"客户端断开连接：{websocket.remote_address}, 原因：{e}")
    except (KeyboardInterrupt, Exception) as e:
        raise e 
    finally:
        print(f"连接结束：{websocket.remote_address}")

async def stream_chat_handler(websocket: Any) -> None:
    try:
        async for message in websocket:
            data = json.loads(message)
            input = data.get("query", "")
            if input == "clear":
                memory.clear()
                await websocket.send(json.dumps({"response": "记忆已被清空"}))
                continue
            if not input:
                await websocket.send(json.dumps({"error": "问题不能为空"}))
            # TODO
            await websocket.send(json.dumps({"response":"暂未实现"}))
    except websockets.ConnectionClosed as e:
        raise ValueError(f"客户端断开连接：{websocket.remote_address}, 原因：{e}")
    except (KeyboardInterrupt, Exception) as e:
        raise e 
    finally:
        print(f"连接结束：{websocket.remote_address}")

ROUTE_HANDLERS = {
    "/chat": chat_handler,
    "/stream_chat": stream_chat_handler
}

async def process_request(connection: Any, request: Any) -> None:
    if request.path not in ROUTE_HANDLERS:
        return (404, [], "路径不存在")
    return None

async def handle_client(websocket: Any) -> None:
    path = websocket.request.path
    print(f"客户端已连接：{websocket.remote_address}, 路径：{path}")
    handler = ROUTE_HANDLERS.get(path)
    if handler:
        await handler(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 8765, process_request=process_request):
        print("WebSocket 服务器已启动，等待连接...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
