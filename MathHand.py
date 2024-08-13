import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from PIL import Image
import streamlit as st

# Initialize the webcam to capture video
cap = cv2.VideoCapture(0)  # Using the default camera
cap.set(3, 1280)  # Set width of the frame
cap.set(4, 720)   # Set height of the frame

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

def getHandInfo(img):
    # Find hands in the current frame
    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand1 = hands[0]
        lmList = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]    # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")
        
        # Count the number of fingers up for the first hand
        fingers1 = detector.fingersUp(hand1)
        return fingers1, lmList 
    else:
        return None

def draw(info,prev_pos,canvas):
    fingers, lmList = info
    current_pos= None
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lmList[8][0:2]
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas,current_pos,prev_pos,(255,0,255),10)
    elif fingers == [1, 0, 0, 0, 0]:
        canvas = np.zeros_like(img)
 
    return current_pos, canvas

prev_pos= None
canvas=None
image_combined = None
output_text= ""


# Continuously get frames from the webcam
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    if canvas is None:
        canvas = np.zeros_like(img)
        
    if success:
        info = getHandInfo(img)
        
        
        if info:
            fingers, lmList = info
            prev_pos,canvas = draw(info, prev_pos,canvas)
            image_combined= cv2.addWeighted(img,0.7,canvas,0.3,0)
        
            print(fingers)  # Output the count of fingers raised
            image_combined= cv2.addWeighted(img,0.7,canvas,0.3,0)

    # Display the image in a window
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", canvas)
    cv2.imshow("image_combined", image_combined)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
