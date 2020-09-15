FROM tensorflow/tensorflow:latest

COPY app.py /app.py
COPY templates /templates
COPY static /static
COPY requirements.txt /requirements.txt
COPY model /model

RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip install -r requirements.txt

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0", "--port", "8080" ]