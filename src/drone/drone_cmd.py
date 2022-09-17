from ctypes import sizeof
import cv2
from djitellopy import Tello
import requests
import time
import json

MAX_IMAGE = 20 # saves last 20 images
MAX_CMD_HISTORY = 5
IMAGE_REFRESH = 10 # set time interval between captures to 10s

LOGIC_API_ENDPOINT = ""

image_name = "capture"
image_index = 0
cmd_history = []
cmd_index = 0
move_mag = 0

# initialize drone
tello = Tello()
tello.connect(False)
tello.streamon()
tello.takeoff()

def get_info(info_type):
    if info_type == "speed":
        return tello.speed()
    elif info_type == "battery":
        return tello.battery()
    elif info_type == "direction":
        return cmd_history[cmd_index]

cmd = requests.get(LOGIC_API_ENDPOINT)
while cmd != "land":
    # get logic commands and parse json
    cmd = json.loads(requests.get(LOGIC_API_ENDPOINT))["data"]

    # damper speed of drone based on command frequency
    for i in range(sizeof(cmd_history)):
        move_mag += cmd_history[i]
    move_mag /= MAX_CMD_HISTORY
    
    # translate logic commands to drone commands
    if cmd == "forward":
        tello.move_forward(move_mag)
    elif cmd == "left":
        tello.move_left(move_mag)
    elif cmd == "right":
        tello.move_right(move_mag)
    else:
        tello.move_back(move_mag)

    cmd_history[cmd_index] = cmd
    cmd_index = cmd_index + 1

    # restrict max size of command buffer
    if sizeof(cmd_history) >= MAX_CMD_HISTORY:
        cmd_index = 0

    # get frame from drone camera
    frame_read = tello.get_frame_read()

    cv2.imwrite(image_name + str(image_index) + ".png", frame_read.frame) # save frame from drone camera
    image_index = image_index + 1
    if image_index >= 20:
        image_index = 0

    time.sleep(IMAGE_REFRESH)

#tello.streamoff()
