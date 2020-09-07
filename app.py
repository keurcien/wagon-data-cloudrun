import falcon
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

class ImageClassifier:

    def __init__(self):
        self.model = load_model("vgg16_model")

    def on_get(self, req, resp):
        img = cv2.imread('DSC01159-2.jpg')
        img = cv2.resize(img,(224,224))
        img = np.reshape(img,[1,224,224,3])
        resp.media = {
            "prediction": str(self.model.predict(img)[0])
        }

api = falcon.API()
api.add_route('/', ImageClassifier())