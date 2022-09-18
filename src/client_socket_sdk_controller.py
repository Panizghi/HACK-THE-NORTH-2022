

# dir = json.loads(requests.get(LOGIC_API_ENDPOINT))['direction']
# while dir != "up":
#     dir = json.loads(requests.get(LOGIC_API_ENDPOINT))['direction']

# tello.takeoff()

# while cmd != "land":
#     # get logic commands and parse json
#     cmd = json.loads(requests.get(LOGIC_API_ENDPOINT))
#     dir = cmd["direction"]
#     mag = cmd["magnitude"]
    
#     # translate logic commands to drone commands
#     if dir == "forward":
#         tello.move_forward(mag)
#     elif dir == "left":
#         tello.move_left(mag)
#     elif dir == "right":
#         tello.move_right(mag)
#     elif dir == "up":
#         tello.move_up(mag)
#     elif dir == "down":
#         tello.move_down(mag)
#     else:
#         tello.move_back(mag)

#     last_cmd = cmd

#     # get frame from drone camera
#     frame_read = tello.get_frame_read()

#     cv2.imwrite("capture" + str(image_index) + ".png", frame_read.frame) # save frame from drone camera
#     image_index = image_index + 1
#     if image_index >= MAX_IMAGE:
#         image_index = 0

#     time.sleep(IMAGE_REFRESH)

# tello.land()
# tello.streamoff()





###

from ctypes import sizeof
import cv2
from djitellopy import Tello
import requests

import asyncio
import websockets
import time
import json



MAX_IMAGE = 20 # saves last 20 images
IMAGE_REFRESH = 10 # set time interval between captures to 10s

LOGIC_API_ENDPOINT = ""

image_index = 0
last_cmd = 0
dir = 0
mag = 0

xi = 0 # forward and back direction
yi = 0 # left and right direction
zi = 0 # up and down direction
xf = 0
yf = 0
zf = 0

# initialize drone
tello = Tello()
tello.connect(False)
tello.streamon()

tello.takeoff()

# default autonomous flight
def default_auto():
    tello.move_forward(50)
    tello.rotate_counter_clockwise(90)
    tello.move_forward(50)
    tello.rotate_counter_clockwise(90)
    tello.move_forward(50)
    tello.rotate_counter_clockwise(90)
    tello.move_forward(50)
    tello.rotate_counter_clockwise(90)

async def connect_to_client():
    async with websockets.connect("ws://localhost:8000/ws/sdk_controller_socket") as websocket:
        while True:
            
            client_data = {"movement": "ok"}
            await websocket.send(json.dumps(client_data))
            server_data = await websocket.recv()
            server_data = json.loads(server_data)
            # print(server_data)
            print(server_data["data"]["commandVector"])

            dir = server_data["data"]["commandVector"]["direction"]
            mag = int(server_data["data"]["commandVector"]["magnitude"])

            # translate logic commands to drone commands

            if dir == "forward":
                xf = xi + mag
                tello.curve_xyz_speed(xi, yi, zi, xf, yf, zf, mag)
            elif dir == "back":
                xf = xi - mag
                tello.curve_xyz_speed(xi, yi, zi, xf, yf, zf, mag)
            elif dir == "left":
                yf = yi - mag
                tello.curve_xyz_speed(xi, yi, zi, xf, yf, zf, mag)
            elif dir == "right":
                yf = yi + mag
                tello.curve_xyz_speed(xi, yi, zi, xf, yf, zf, mag)
            elif dir == "up":
                zf = zi + mag
                tello.curve_xyz_speed(xi, yi, zi, xf, yf, zf, mag)
            elif dir == "down":
                zf = zi - mag
                tello.curve_xyz_speed(xi, yi, zi, xf, yf, zf, mag)
            elif dir == "rotate_left":
                tello.rotate_counter_clockwise(mag)
            elif dir == "rotate_right":
                tello.rotate_clockwise(mag)
            else:
                # hover
                pass
            
            xi = xf
            yi = yf
            zi = zf

asyncio.run(connect_to_client())
