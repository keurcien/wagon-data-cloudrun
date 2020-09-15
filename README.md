# wagon-data-cloudrun

This repository contains a simple example of a Flask app that serves a
Deep Learning model (VGG16 in this case): https://image-classifier-sdauzsikga-ew.a.run.app/.
Now that Cloud Run instances can be configured with 4GB of RAM, it makes it a viable option for
Deep Learning deployment, especially for Minimum Viable Products. But before you proceed:

- Make sure you have a Google Cloud project set up.
- Docker and gcloud CLI are installed on your local machine

## Google Container Registry

Google Container Registry is a Google service designed to host your Docker images.
It allows other services such as Cloud Run to access these images in a convenient way.

- Go to your Google Cloud project
- Enable Google Container Registry API
- Open a terminal and run the following commands:

```shell
# Choose the Google account associated with your Google Cloud project
gcloud auth login
# Create JSON credentials
gcloud auth configure-docker
# Set the project name
export PROJECT_ID = project_id # pick it up from your Google Cloud console
gcloud config set project $PROJECT_ID
```

You should be good to go.

## Let's take a look at the app

```python
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
```

All you need is a model that you can load. It is loaded outside of the `index` scope so it does not
get loaded everytime a request is processed.

## requirements.txt

List all the dependencies needed to run your app.

## Build the Docker image


```shell
export DOCKER_IMAGE_NAME = docker_image_name # name it like you want e.g. image_classifier
docker build -t eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME .
```

Make sure your image runs:

```shell
docker run -p 8080:8080 eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```
Have a lookup at [http://localhost:8080](http://localhost:8080)

Push the docker image on Google Cloud Registry:

```shell
docker push eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```

## Deploy on Cloud Run

```shell
gcloud run deploy --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME --platform managed --region europe-west1
```
