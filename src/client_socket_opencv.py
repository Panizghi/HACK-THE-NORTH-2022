import asyncio
# from distutils.cmd import Command
# from tkinter import Y
# from unittest.runner import _ResultClassType
import websockets
import time
import json

# program-specific
import cv2
import mediapipe as mp
from tensorflow.keras.models import load_model
import numpy as np
import math

cap = cv2.VideoCapture(0)

mp_hands_collection = mp.solutions.hands
hands_model = mp_hands_collection.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw_obj = mp.solutions.drawing_utils


hand_gesture_model = load_model("static/mp_hand_gesture")

gesture_names_file = open("static/gesture.names", "r")
class_names = gesture_names_file.read().split("\n")

gesture_names_file.close()



class CommandPrediction:

    def __init__(self, hand_gesture_model, class_names, landmarks, X_CONST, Y_CONST):
        self.landmarks = landmarks
        self.hand_gesture_model = hand_gesture_model
        self.class_names = class_names
        self.class_name = None
        self.return_resp = {
            "direction": None,
            "magnitude": None,
            "context": "opencv"
        }

        self.X_CENTER_CONST = 0.5
        self.Y_CENTER_CONST = 0.5

        self.X_CONST = X_CONST
        self.Y_CONST = Y_CONST

        print(np.mean([x[0] for x in landmarks]))
        print(np.mean([x[1] for x in landmarks]))

        print(self.class_names)

        self.landmarks_for_pred = [[x[0]*self.X_CONST, x[1]*self.Y_CONST] for x in self.landmarks]

        self.x_centroid_curr = np.mean([x[0] for x in landmarks])
        self.y_centroid_curr = np.mean([x[1] for x in landmarks])


    def compute_direction_and_magnitude(self, class_name):
        pred_vector = {"direction": "hover", "magnitude": 0, "predictedClass": class_name}

        if class_name == "fist":
            if self.y_centroid_curr < 0.3:
                pred_vector["direction"] = "up"
            elif self.y_centroid_curr > 0.7:
                pred_vector["direction"] = "down"
            elif self.x_centroid_curr < 0.3:
                pred_vector["direction"] = "left"
            elif self.x_centroid_curr > 0.7:
                pred_vector["direction"] = "right"

        elif class_name == "rock":
            if self.y_centroid_curr < 0.3:
                pred_vector["direction"] = "forward"
            elif self.y_centroid_curr > 0.7:
                pred_vector["direction"] = "backward"
            elif self.x_centroid_curr < 0.3:
                pred_vector["direction"] = "rotate_left"
            elif self.x_centroid_curr > 0.7:
                pred_vector["direction"] = "rotate_right"
        
        pred_vector["magnitude"] = round(math.sqrt((0.5-self.x_centroid_curr)**2+(0.5-self.y_centroid_curr)**2),3)

        return pred_vector

    def return_prediction(self):
        prediction = self.hand_gesture_model.predict([self.landmarks_for_pred])
        print(prediction)
        class_id = np.argmax(prediction)
        print(class_id, self.class_names)
        self.class_name = self.class_names[class_id]

        return self.compute_direction_and_magnitude(self.class_name)


async def connect_to_client():
    async with websockets.connect("ws://localhost:8000/ws/opencv_socket") as websocket:



        while True:
            _, frame = cap.read()
            x, y, c = frame.shape

            frame = cv2.flip(frame, 1)


            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands_model.process(frame_rgb)


            predicted_vector = {"direction": "hover", "magnitude": 0, "predictedClass": None}

            if result.multi_hand_landmarks:
                landmarks = []
                count = 1
                for hand_landmarks in result.multi_hand_landmarks:
                    # print(count)
                    count += 1
                    for landmark in hand_landmarks.landmark:
                        landmarks.append([landmark.x, landmark.y])

                    # print(landmarks)

                    mp_draw_obj.draw_landmarks(frame, hand_landmarks, mp_hands_collection.HAND_CONNECTIONS)
                
                    command_obj = CommandPrediction(hand_gesture_model=hand_gesture_model, class_names=class_names, landmarks=landmarks, X_CONST=x, Y_CONST=y)
                    predicted_vector = command_obj.return_prediction()

                    # print(predicted_vector)

                    # prediction = hand_gesture_model.predict([landmarks])
                    # class_id = np.argmax(prediction)
                    # class_name = class_names[class_id]

                    # print(class_name)

                cv2.putText(frame, str(predicted_vector), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA)

            # opencv ui
            cv2.imshow("Drone Human Interface", frame)
            
            ### WEBSOCKET
            client_data = predicted_vector
            await websocket.send(json.dumps(client_data))
            server_data = await websocket.recv()
            print(server_data)


            # QUIT OPENCV
            if cv2.waitKey(1) == ord("q"):
                break


# async def connect_to_client():
#     async with websockets.connect("ws://localhost:8000/ws/opencv_socket") as websocket:
#         while True:

#             _, frame = cap.read()
#             x, y, c = frame.shape

#             frame = cv2.flip(frame, 1)

#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             result = hands_model.process(frame_rgb)

#             class_name = ""

#             if result.multi_hand_landmarks:
#                 landmarks = []
#                 for hand_landmarks in result.multi_hand_landmarks:
#                     for landmark in hand_landmarks.landmark:
#                         print(landmark)
#                         landmarks.append([int(landmark.x*x), int(landmark.y*y)])

#                     mp_draw_obj.draw_landmarks(frame, hand_landmarks, mp_hands_collection.HAND_CONNECTIONS)

#                     prediction = hand_gesture_model.predict([landmarks])
#                     class_id = np.argmax(prediction)
#                     class_name = class_names[class_id]

#                 cv2.putText(frame, class_name, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

#             cv2.imshow("Drone Human Interface", frame)

#             client_data = {"movement": "ok"}
#             await websocket.send(json.dumps(client_data))
#             server_data = await websocket.recv()
#             print(server_data)
#             time.sleep(0.5)

asyncio.run(connect_to_client())

cap.release()
cv2.destroyAllWindows()