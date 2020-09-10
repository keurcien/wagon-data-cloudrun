# wagon-data-cloudrun

This repository contains a simple boilerplate to quickly build a
falcon API ready to be deployed with Cloud Run. Now that Cloud Run instances
can be configured with 4GB of RAM, it makes it a serious option for
Deep Learning deployment. But before you proceed:

- Make sure you have a Google Cloud project set up.
- Docker and gcloud CLI are installed on your local machine

## Google Container Registry

Google Container Registry is a Google service designed to host your Docker images.
It allows other services such as Cloud Run to access these images in a convenient way.

- Go to your Google Cloud project
- Enable Google Container Registry API
- Open a terminal and run the following commands:

```shell
gcloud auth login
gcloud auth configure-docker
```

- Choose the Google account associated with your Google Cloud project.

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
docker build -t eu.gcr.io/[project_id]/[docker_image_name] .
docker push eu.gcr.io/[project_id]/[docker_image_name]
```

Make sure your image runs:

```shell
docker run -p 8080:8080 eu.gcr.io/[project_id]/[docker_image_name]
```

## Deploy on Cloud Run

Go to your Google Cloud Platform project and open the service panel.
Select the Cloud Run service and create a new service.