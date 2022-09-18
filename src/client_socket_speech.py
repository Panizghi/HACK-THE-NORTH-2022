import pyaudio
 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

import websockets
import asyncio
import base64
import json
import os 
import time



class SpeechCommandPrediction:

    def __init__(self):
        self.pred_vector = {
            "direction": "hover",
            "magnitude": 0.0,
            "context": "speech"
        }
        self.client_text = ""
        self.keyword = ""

    def process_client_text(self, client_text):
        return client_text.replace(".", "").lower()
    
    def push_text(self, client_text):
        self.client_text = client_text
        self.keyword = self.process_client_text(self.client_text)

    def return_prediction(self):

        if self.keyword == "take off":
            self.pred_vector["direction"] = "top"
            self.pred_vector["magnitude"] = 20.0

        elif self.keyword == "land":
            self.pred_vector["direction"] = "bottom"
            self.pred_vector["magntidue"] = 20.0

        elif self.keyword == "forward":
            self.pred_vector["direction"] = "forward"
            self.pred_vector["magnitude"] = 20.0

        elif self.keyword == "backward":
            self.pred_vector["direction"] = "backward"
            self.pred_vector["magnitude"] = 20.0

        elif self.keyword == "left":
            self.pred_vector["direction"] = "left"
            self.pred_vector["magnitude"] = 20.0

        elif self.keyword == "right":
            self.pred_vector["direction"] = "right"
            self.pred_vector["magnitude"] = 20.0

        elif self.keyword == "top":
            self.pred_vector["direction"] = "top"
            self.pred_vector["magnitude"] = 20.0

        elif self.keyword == "bottom":
            self.pred_vector["direction"] = "bottom"
            self.pred_vector["magnitude"] = 20.0

        elif self.keyword == "stop" or self.keyword == "hover":
            self.pred_vector["direction"] = "hover"
            self.pred_vector["magnitude"] = 0.0
        

        return self.pred_vector

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

master_data_dict = {
    "client_text": ""
}

async def connect_to_master_api():

    
    client_data = {
        "data": {
            "movement": "ok",
            "commandVector": {
                "direction": "hover",
                "magnitude": 0.0,
                "context": "speech"
            }
        }
    }

    async with websockets.connect("ws://localhost:8000/ws/speech_socket") as websocket:
        while True:


            if len(master_data_dict["client_text"]) > 0:
                speech_cmd_pred_obj = SpeechCommandPrediction()
                speech_cmd_pred_obj.push_text(master_data_dict["client_text"])
                client_data["commandVector"] = speech_cmd_pred_obj.return_prediction()

            await websocket.send(json.dumps(client_data))
            server_data = await websocket.recv()
            print(server_data)





async def connect_to_client():
    print(f'Connecting websocket to url ${URL}')
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", os.getenv("AAI_API_KEY")),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")
        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data":str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)
            
            return True
      
        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    if json.loads(result_str)["message_type"] == "FinalTranscript":
                        print(json.loads(result_str)['text'])
                        master_data_dict["client_text"] = json.loads(result_str)["text"]
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
      
        send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(connect_to_client())
