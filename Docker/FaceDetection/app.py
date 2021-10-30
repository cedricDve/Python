import cv2
import random, os
#Flask will launch this app by default (app.py)
from flask import Flask, render_template, url_for

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--path",default="static")
args = parser.parse_args()

# Load pre-trained data (frontal face detection) | haarcascade algorithm
trained_face_data = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')


app = Flask(__name__,static_folder=args.path)

#Home page
@app.route('/')
def home():
    return render_template('index.html')


# Show image with Facedetection
@app.route('/facedetection-image')
def facedetection_image():
    path = os.path.join(args.path,"image-facedetection.jpg")
    return "<img src="+path+"/>"

#Face detection on standard family image
@app.route('/facedetection')
def facedetection():
    
    img = cv2.imread('./static/image.jpg')
    
    grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# Note RGB is BGR in OpenCV !

    face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)

    for (x,y,w,h) in face_coordinates:
        cv2.rectangle(img ,(x,y) , (x +w , y+h), (random.randrange(128,256),random.randrange(256),random.randrange(256)), 2 )

    result = cv2.imwrite('./static/image-facedetection.jpg', img)

    if result == True:  
        print("Image saved correctly")

    return render_template('facedetection-image.html')

#Face detection on a random image
@app.route('/facedetection-random')
def facedetection_random():
    random_image = str(random.randrange(1,5))
    print(random_image)

    img = cv2.imread(f"./static/{random_image}.jpg")
    
    grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# Note RGB is BGR in OpenCV !

    face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)

    for (x,y,w,h) in face_coordinates:
        cv2.rectangle(img ,(x,y) , (x +w , y+h), (random.randrange(128,256),random.randrange(256),random.randrange(256)), 2 )

    result = cv2.imwrite(f'./static/image-facedetection-{random_image}.jpg', img)

    if result == True:  
        print("Image saved correctly")
        
    path = os.path.join(args.path,f"image-facedetection-{random_image}.jpg")
    return "<img src="+path+"/>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')