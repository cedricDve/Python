import cv2
import random

import pygame

# Load pre-trained data (frontals face detection) | haarcascade algorithm
trained_face_data = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# Get webcam video to detect face -> cv2.VideoCapture(0) 
# -- 0 = default (webcam!)
webcam = cv2.VideoCapture("./video-1.mp4") 

# loop through all frames of the video (webcam)
run = True 

while run:

    # Read the current frame
    # -- succesful_frame_read should  always be true
    succesful_frame_read, frame = webcam.read()
    grayscaled_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)

    for (x,y,w,h) in face_coordinates:
        # Draw rectangle
        cv2.rectangle(frame ,(x,y) , (x +w , y+h), (random.randrange(128,256),random.randrange(256),random.randrange(256)), 2 )

    cv2.imshow('Family Image FACE DETECTOR', frame)
    cv2.waitKey(1)







#print(face_coordinates) # coordinates of the face that is detected

# -- let cv2 show image untill a key is pressed





print("Code Completed")