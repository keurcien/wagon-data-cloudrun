import cv2
import base64
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from flask import Flask, request, render_template

def crop_image(img):
    target_size = np.min(img.shape[0:2])
    return img[0:target_size, 0:target_size, :]

def process_request_image(img):
    img_ = np.fromstring(img, np.uint8)
    img_ = cv2.imdecode(img_, cv2.IMREAD_COLOR)
    return crop_image(img_)

def create_data_uri(img):
    _, img_ = cv2.imencode('.jpg', img)
    img_ = img_.tobytes()
    img_ = base64.b64encode(img_)
    img_ = img_.decode()
    mime = "image/jpeg"
    return "data:%s;base64,%s" % (mime, img_)

model = VGG16(weights='imagenet')

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html', prediction=None, img=None)

    if request.method == 'POST':

        # Handle request
        img = request.files['file'].read()

        # A tiny bit of preprocessing
        img = process_request_image(img)
        
        # Convert image to data URI so it can be displayed without being saved
        uri = create_data_uri(img)
        
        # Convert to VGG16 input
        img = cv2.resize(img, (224, 224))
        img = np.reshape(img, [1, 224, 224, 3])

        # Classify image
        predictions = model.predict(img)
        labels = decode_predictions(predictions, top=1)

        return render_template('index.html', prediction=labels[0][0][1], img=uri)
