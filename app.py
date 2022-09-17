from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/")
async def home():
    data = {"data": "The world's first hands-free, multi-purpose drone."}
    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

