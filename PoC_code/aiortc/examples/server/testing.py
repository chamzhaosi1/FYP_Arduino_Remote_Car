# STEP 1: Import the necessary modules.
import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection.FaceDetection()
mp_drawing = mp.solutions.drawing_utils

# Load the input image
image = cv2.imread('static/unknowImg/Jacky.jpg')

# img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = mp_face_detection.process(image)

if results.detections:
    for dectection in results.detections:
        mp_drawing.draw_detection(image, dectection)

cv2.imwrite("testing.jpg", image)

