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

@app.websocket("/ws/speech_socket")
async def ws_speech_socket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = {"data": {"status":"speech is received", "clientMsg": ""}}
        client_data = await websocket.receive_text()
        client_data_json = json.loads(client_data)
        data["data"]["clientMsg"] = client_data_json
        await websocket.send_text(json.dumps(data))


@app.websocket("/ws/opencv_socket")
async def ws_opencv_socket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = {"data": {"status":"opencv is received", "clientMsg": ""}}
        client_data = await websocket.receive_text()
        client_data_json = json.loads(client_data)
        data["data"]["clientMsg"] = client_data_json
        await websocket.send_text(json.dumps(data))


@app.websocket("/ws/sdk_controller_socket")
async def ws_controller_socket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = {"data": {"status": "SDK controller is received", "clientMsg": ""}}
        client_data = await websocket.receive_text()
        client_data_json = json.loads(client_data)
        data["data"]["clientMsg"] = client_data_json
        await websocket.send_text(json.dumps(data))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

