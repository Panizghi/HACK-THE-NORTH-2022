import asyncio
import websockets
import time
import json


async def connect_to_client():
    async with websockets.connect("ws://localhost:8000/ws/opencv_socket") as websocket:
        while True:

            client_data = {"movement": "ok"}
            await websocket.send(json.dumps(client_data))
            server_data = await websocket.recv()
            print(server_data)
            time.sleep(0.1)

asyncio.run(connect_to_client())
