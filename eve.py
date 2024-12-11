import asyncio
import subprocess
import signal
import sys

processes = []

async def start_webui():
    process = subprocess.Popen(["python", "web/app.py"])
    processes.append(process)

async def start_websocket():
    process = subprocess.Popen(["python", "websocket_api.py"])
    processes.append(process)

async def main():
    await asyncio.gather(start_websocket(), start_webui())

def cleanup():
    for process in processes:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    print("服务已全部停止")
    sys.exit(0)
global_loop = asyncio.new_event_loop()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
if __name__ == "__main__":
    import threading
    threading.Thread(target=start_loop, args=(global_loop,), daemon=True).start()

    signal.signal(signal.SIGINT, lambda *args: cleanup())
    signal.signal(signal.SIGTERM, lambda *args: cleanup())
    main_loop = asyncio.new_event_loop()
    try:
        while True:
            main_loop.run_until_complete(asyncio.sleep(3600))
    except KeyboardInterrupt:
        cleanup()
