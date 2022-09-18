from ctypes import sizeof
import cv2
from djitellopy import Tello
import requests
import time
import json

MAX_IMAGE = 20 # saves last 20 images
IMAGE_REFRESH = 10 # set time interval between captures to 10s

LOGIC_API_ENDPOINT = ""

image_index = 0
last_cmd = 0
dir = 0
mag = 0

# initialize drone
tello = Tello()
tello.connect(False)
tello.streamon()

dir = json.loads(requests.get(LOGIC_API_ENDPOINT))['direction']
while dir != "up":
    dir = json.loads(requests.get(LOGIC_API_ENDPOINT))['direction']

tello.takeoff()

while cmd != "land":
    # get logic commands and parse json
    cmd = json.loads(requests.get(LOGIC_API_ENDPOINT))
    dir = cmd["direction"]
    mag = cmd["magnitude"]
    
    # translate logic commands to drone commands
    if dir == "forward":
        tello.move_forward(mag)
    elif dir == "left":
        tello.move_left(mag)
    elif dir == "right":
        tello.move_right(mag)
    elif dir == "up":
        tello.move_up(mag)
    elif dir == "down":
        tello.move_down(mag)
    else:
        tello.move_back(mag)

    last_cmd = cmd

    # get frame from drone camera
    frame_read = tello.get_frame_read()

    cv2.imwrite("capture" + str(image_index) + ".png", frame_read.frame) # save frame from drone camera
    image_index = image_index + 1
    if image_index >= MAX_IMAGE:
        image_index = 0

    time.sleep(IMAGE_REFRESH)

tello.land()
tello.streamoff()
