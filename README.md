# wagon-data-cloudrun

This repository contains a simple boilerplate to quickly build a
falcon API with Docker and gunicorn. It can be easily deployed on
Cloud Run for example, provided that you own a Google Cloud Platform
project. Now that Cloud Run instances can be configured with 4GB of RAM,
it makes it a serious option for Deep Learning deployment.

## Let's take a look at the app

```python
import falcon
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

class ImageClassifier:

    def __init__(self):
        '''Falcon API entrypoint.
        
        In short, it is a regular class with specific methods such as
        on_get or on_post.
        '''
        self.model = load_model("vgg16_model")

    def on_get(self, req, resp):
        img = cv2.imread('DSC01159-2.jpg')
        img = cv2.resize(img,(224,224))
        img = np.reshape(img,[1,224,224,3])
        resp.media = {
            "prediction": str(self.model.predict(img)[0])
        }

# Instantiate a falcon API
api = falcon.API()

# API routing
api.add_route('/', ImageClassifier())
```

All you need is a model that you can load.

## requirements.txt

List all the dependencies needed to run your app.

## Build the Docker image

```
docker build -t eu.gcr.io/[project_name]/[image_name] .
docker push eu.gcr.io/[project_name]/[image_name]
```

## Deploy on Cloud Run

Go to your Google Cloud Platform project and open the service panel.
Select the Cloud Run service and create a new service.

