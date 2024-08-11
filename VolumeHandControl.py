import cv2
import time
import numpy as np

# Camera settings
wCam, hCam = 1280, 720

# Initialize the camera capture object with the cv2.VideoCapture class.
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

# Set the width and height of the capture
cap.set(3, wCam)
cap.set(4, hCam)

while True:
    # Capture frame-by-frame
    success, img = cap.read()

    # If frame is read correctly, show it
    if success:
        cv2.imshow("Img", img)
    else:
        print("Error: Frame could not be retrieved.")
        break

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

