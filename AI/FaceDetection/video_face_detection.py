import cv2
import random

# Load pre-trained data (frontals face detection) | haarcascade algorithm
trained_face_data = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# Get webcam video to detect face -> cv2.VideoCapture('path/to/file')    
webcam = cv2.VideoCapture("./video/video-1.mp4")# 0 = default (webcam!)

# Loop through all frames of the video (webcam)
run = True 
while run:
    # Read the current frame
    succesful_frame_read, frame = webcam.read()# -- succesful_frame_read should  always be true
    grayscaled_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces
    face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)
    # Draw rectangles -> face detection
    for (x,y,w,h) in face_coordinates:
        cv2.rectangle(frame ,(x,y) , (x +w , y+h), (random.randrange(128,256),random.randrange(256),random.randrange(256)), 2 )

    # Show video
    cv2.imshow('Family Image FACE DETECTOR', frame)
    cv2.waitKey(1) # -- let cv2 show image untill a key is pressed

    #print(face_coordinates) # coordinates of the face that is detected
# End
print("Code Completed")