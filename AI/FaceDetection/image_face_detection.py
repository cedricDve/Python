import cv2
import random
import csv

# Load pre-trained data (Frontal face detection) 
# -- Haarcascade algorithm
trained_face_data = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
# Get image: cv2 image read function -> imread()
img = cv2.imread('./images/mask4.jpg')
# Change image to grayscale  !important step
# -- Using convert color function of cv2 -> cvtColor(src, mode)
grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# Note RGB is BGR in OpenCV !
# Detect faces
# -- detectMultiScale: independing the size of the image, face will be detected
face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)

# Draw rectangle: top-left coordinates (x,y)
for (x,y,w,h) in face_coordinates:
    # Draw rectangle for each face
    cv2.rectangle(img ,(x,y) , (x +w , y+h), (random.randrange(128,256),random.randrange(256),random.randrange(256)), 2 )

# Show image with facial detection
cv2.imshow('Family Image FACE DETECTOR', img)

# Save image
result = cv2.imwrite('./images/image-facedetection.jpg', img)
if result == True:  
    print("Image saved correctly")
# Save face coordinates into csv file
with open('./facial-detection.csv', 'w') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(face_coordinates)

cv2.waitKey()# -- let cv2 show the image, untill a key is pressed
# End
print("Code Completed")
cv2.destroyAllWindows()# --De-allocate any associated memory usage