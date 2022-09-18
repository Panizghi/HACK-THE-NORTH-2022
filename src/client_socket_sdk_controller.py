import asyncio
import websockets
import time
import json

async def connect_to_client():
    async with websockets.connect("ws://localhost:8000/ws/sdk_controller_socket") as websocket:
        while True:
            
            client_data = {"movement": "ok"}
            await websocket.send(json.dumps(client_data))
            server_data = await websocket.recv()
            print(server_data)

asyncio.run(connect_to_client())
