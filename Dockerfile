FROM python:3.7-slim-buster

COPY app.py /app.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8080", "app:api" ]