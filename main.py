import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

cap = cv2.VideoCapture(0)

mp_hands_collection = mp.solutions.hands
hands_model = mp_hands_collection.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw_obj = mp.solutions.drawing_utils


hand_gesture_model = load_model("static/mp_hand_gesture")

gesture_names_file = open("static/gesture.names", "r")
class_names = gesture_names_file.read().split("\n")

gesture_names_file.close()

print(class_names)
print("Entering loop. Press the Q key to exit.")


while True:
    _, frame = cap.read()
    x, y, c = frame.shape

    frame = cv2.flip(frame, 1)


    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands_model.process(frame_rgb)

    class_name = ""

    if result.multi_hand_landmarks:
        landmarks = []
        for hand_landmarks in result.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                landmarks.append([int(landmark.x*x), int(landmark.y*y)])

            mp_draw_obj.draw_landmarks(frame, hand_landmarks, mp_hands_collection.HAND_CONNECTIONS)
        
            prediction = hand_gesture_model.predict([landmarks])
            class_id = np.argmax(prediction)
            class_name = class_names[class_id]

        cv2.putText(frame, class_name, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    cv2.imshow("Hand Gesture Demo", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
