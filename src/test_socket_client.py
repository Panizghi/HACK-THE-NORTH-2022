import asyncio
import websockets
import time
import random

async def hello():
    async with websockets.connect("ws://localhost:8000/ws/get_drone_motor_sdk_command") as websocket:
        while True:
            await websocket.send(str(random.randrange(0,100)))
            data = await websocket.recv()
            print(data)
            time.sleep(0.1)

asyncio.run(hello())
