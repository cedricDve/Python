# FACE DETECTION

Face detection with `Python`
1. Get many images of Faces 
2. Make them black-and-white (gray-scale)| colors are not important

> OpenCV: Opensource Computer Vision library 

3. Train the algorithm to detect faces

## Objective
Learn more about how to use cv2 with python. 
Experiment with how to implement facial face detection on a different type of media.

## Program

## OpenCV documentation
https://vovkos.github.io/doxyrest-showcase/opencv/sphinx_rtd_theme/index.html
### Install OpenCV
`pip install opencv-python`

Import opencv using `import cv2`

### Haarcascade algorithm

>Using haarcascade algorithm with prebuild datafiles, from github:
https://github.com/opencv/opencv/tree/master/data/haarcascades

`haarcascade_frontalface_default.xml`

## Facial Face Detection - static image

1. Load pre-trained data of frontal-face-detections
    
    `trained_face_data = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')`

    >Note: We use CascadeClassifier (to detect object), a OpenCV function that expect a path to the file that contains pre-trained data.

2. Choose an image to try-out our face-detection
    
    `img = cv2.imread('./image.jpg')`

    >Note: We use imread, a OpenCv function that allows us to read an image.

3. We must grayscale our image !
    
    `grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# Note RGB is BGR in OpenCV !`

    >Note: We use cvtColor, an OpenCV function that allows us to convert an image.
    cvtColor(src, dst, code, dstCN )
    
    Code for grayscaled image:`` COLOR_BGR2GRAY``

4. Detect face on selected image
    
    `face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)`

    >Note: We use detectMultiScale. Detects object independing the size of the image(input). The detected objects are returned as a list of rectangles.

5. Show result: show grayscaled image

    `cv2.imshow('Family Image FACE DETECTOR', grayscaled_img)`

    `cv2.waitKey()`

6. Draw rectangle around the detected face (on the image)

    Note: we don't know how many faces there will be on the image. Therefore we loop through our face_coordinates (array).

    `for (x,y,w,h) in face_coordinates:`
    
    `cv2.rectangle(grayscaled_img ,(x,y) , (x +w , y+h), (0,255,0), 2 )`



## Video face detection

### Real-time face detection using webcam

``webcam = cv2.VideoCapture(0) ``

> Note: 0 means default => webcam 


### Real-time face detection using a video file

``webcam = cv2.VideoCapture('path/to/file') ``