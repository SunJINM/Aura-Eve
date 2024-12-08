import asyncio
import websockets
import json
from lib.llms import Ollama, ZhiPuAI
from lib.memory import ConversationBufferMemory
from lib.chains import LLMChain
from lib.output_parsers import RegexParser
from eve.prompts.prompt import PROMPT

llm = ZhiPuAI()
memory = ConversationBufferMemory(human_prefix="Jin", ai_prefix="eve")
chat_chain = LLMChain(memory=memory, prompt=PROMPT, llm=llm)
parser = RegexParser(regex=r"(.*?)（(.*?)）：(.*)", output_keys=["name", "mode", "content"], default_output_key="content")

async def handle_client(websocket: websockets.ClientProtocol) -> None:
    print(f"客户端已连接：{websocket.remote_address}")
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
            output = chat_chain.run(input=input)
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

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket 服务器已启动，等待连接...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
