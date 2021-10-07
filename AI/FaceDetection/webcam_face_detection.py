import cv2
import random

# Load pre-trained data (frontals face detection) | haarcascade algorithm
trained_face_data = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# Get webcam video to detect face -> cv2.VideoCapture(0) 
# -- 0 = default (webcam!)
webcam = cv2.VideoCapture(0) 

# loop through all frames of the video (webcam)
while True:

    # Read the current frame
    # -- succesful_frame_read should  always be true
    succesful_frame_read, frame = webcam.read()
    grayscaled_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Family Image FACE DETECTOR', grayscaled_img)
    cv2.waitKey()


# Detect faces
# -- detectMultiScale: independing the size of the image, face will be detected
face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)

# Draw rectangle: top-left coordinates (x,y)

for (x,y,w,h) in face_coordinates:
    # Draw rectangle
    cv2.rectangle(img ,(x,y) , (x +w , y+h), (random.randrange(128,256),random.randrange(256),random.randrange(256)), 2 )

# Show grayscaled image




#print(face_coordinates) # coordinates of the face that is detected

# -- let cv2 show image untill a key is pressed





print("Code Completed")