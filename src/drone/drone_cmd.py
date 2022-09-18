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
last_cmd = 0
dir = 0
mag = 0

# initialize drone
tello = Tello()
tello.connect(False)
tello.streamon()
tello.takeoff()

cmd = requests.get(LOGIC_API_ENDPOINT)
while cmd != "land":
    # get logic commands and parse json
    cmd = json.loads(requests.get(LOGIC_API_ENDPOINT))
    dir = cmd["direction"]
    mag = cmd["magnitude"]
    
    # translate logic commands to drone commands
    if cmd == "forward":
        tello.move_forward(mag)
    elif cmd == "left":
        tello.move_left(mag)
    elif cmd == "right":
        tello.move_right(mag)
    else:
        tello.move_back(mag)

    last_cmd = cmd

    # get frame from drone camera
    frame_read = tello.get_frame_read()

    cv2.imwrite(image_name + str(image_index) + ".png", frame_read.frame) # save frame from drone camera
    image_index = image_index + 1
    if image_index >= 20:
        image_index = 0

    time.sleep(IMAGE_REFRESH)

#tello.streamoff()
