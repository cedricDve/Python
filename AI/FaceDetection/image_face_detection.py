import cv2
import random

# Load pre-trained data (frontals face detection) | haarcascade algorithm
trained_face_data = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# Get image to detect face on -> cv2 image read function -> imread()
#img = cv2.imread('./image.jpg')
img = cv2.imread('./image2.jpg')

# Change image to grayscale !
# -- Using convert color function of cv2 -> cvtColor(src, mode)
grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# Note RGB is BGR in OpenCV !

# Detect faces
# -- detectMultiScale: independing the size of the image, face will be detected
face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)

# Draw rectangle: top-left coordinates (x,y)

for (x,y,w,h) in face_coordinates:
    # Draw rectangle
    cv2.rectangle(img ,(x,y) , (x +w , y+h), (random.randrange(128,256),random.randrange(256),random.randrange(256)), 2 )

# Show grayscaled image
cv2.imshow('Family Image FACE DETECTOR', img)



#print(face_coordinates) # coordinates of the face that is detected

# -- let cv2 show image untill a key is pressed
cv2.waitKey()




print("Code Completed")