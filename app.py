from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
import uvicorn
import json

app = FastAPI()

@app.get("/")
async def home():
    data = {"data": "The world's first hands-free, multi-purpose drone."}
    return JSONResponse(content=data)

@app.websocket("/ws/get_drone_motor_sdk_command")
async def ws_get_drone_motor_sdk_command(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = {"data": "go_straight"}
        await websocket.receive_text()
        await websocket.send_text(json.dumps(data))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

