FROM python:3.8-buster

COPY ./requirements.txt /
RUN pip install -U pip && \
    pip install setuptools wheel && \
    pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD gunicorn --bind 0.0.0.0:5000 app:app
