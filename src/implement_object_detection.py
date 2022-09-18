import numpy as np
import cv2

classNames = { 0: "background",
    1: "aeroplane", 2: "bicycle", 3: "bird", 4: "boat",
    5: "bottle", 6: "bus", 7: "car", 8: "cat", 9: "chair",
    10: "cow", 11: "diningtable", 12: "dog", 13: "horse",
    14: "motorbike", 15: "person", 16: "pottedplant",
    17: "sheep", 18: "sofa", 19: "train", 20: "tvmonitor" }


net = cv2.dnn.readNetFromCaffe("static/mobilenet/MobileNetSSD_deploy.prototxt", "static/mobilenet/MobileNetSSD_deploy.caffemodel")

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    frame_resized = cv2.resize(frame, (300,300))

    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)

    net.setInput(blob)
    detections = net.forward()

    cols = frame_resized.shape[1]
    rows = frame_resized.shape[0]

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.8:
            class_id = int(detections[0, 0, i, 1])

            heightFactor = frame.shape[0]/300.0
            widthFactor = frame.shape[1]/300.0

            xLeftBottom = int(detections[0,0,i,3]*cols*widthFactor)
            yLeftBottom = int(detections[0,0,i,4]*rows*heightFactor)
            xRightTop = int(detections[0,0,i,5]*cols*widthFactor)
            yRightTop = int(detections[0,0,i,6]*rows*heightFactor)

            cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop), (0,255,0))

            if class_id in classNames:
                label = classNames[class_id] + ": " + str(confidence)
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                yLeftBottom = max(yLeftBottom, labelSize[1])
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                    (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                    (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xLeftBottom, yLeftBottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))

                print(label)
    print("done")

    cv2.imshow("Drone Camera View", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break
