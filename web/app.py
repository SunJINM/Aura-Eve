from typing import Any, List
import gradio as gr
from pydantic import BaseModel, ConfigDict
import websockets
import asyncio
import json


class WebSocketClient(BaseModel):
    uri: str
    websocket: Any = None
    lock: asyncio.Lock = asyncio.Lock()

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True
    )

    async def connect(self) -> None:
        if not self.websocket:
            self.websocket = await websockets.connect(self.uri)
    
    async def send_message(self, input: str) -> str:
        if self.websocket is None:
            await self.connect()
        async with self.lock:
            await self.websocket.send(json.dumps({"query": input}))
            response = await self.websocket.recv()
        data = json.loads(response).get("response")
        return data

ws_client = WebSocketClient(uri="ws://localhost:8765/chat")
global_loop = asyncio.new_event_loop()

async def websocket_chat(input: str, history: List) -> str:
    data = await ws_client.send_message(input)
    history.append({"role": "user", "content": input})
    history.append({"role": "assistant", "content": data})
    return "", history
    
def chat_with_websocket(user_input: str, history: str) -> str:
    future = asyncio.run_coroutine_threadsafe(
        websocket_chat(user_input, history), global_loop
    )
    return future.result()

def clear_memory() -> None:
    future = asyncio.run_coroutine_threadsafe(
        ws_client.send_message("clear"), global_loop
    )
    future.result()

with gr.Blocks() as demo:
    gr.Markdown("# eve 聊天")
    chatbot = gr.Chatbot(label="聊天记录", type="messages")
    msg = gr.Textbox(placeholder="请输入你的问题...", label="用户输入")
    clear = gr.Button("清空记忆对话")

    msg.submit(chat_with_websocket, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: (None, []), inputs=None, outputs=[msg, chatbot])
    clear.click(clear_memory)


if __name__ == "__main__":
    import threading

    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    threading.Thread(target=start_loop, args=(global_loop,), daemon=True).start()
    demo.launch()
