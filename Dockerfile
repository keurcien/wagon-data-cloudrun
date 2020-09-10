FROM python:3.7-buster

COPY app.py /app.py
COPY templates /templates
COPY static /static
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0", "--port", "8080" ]