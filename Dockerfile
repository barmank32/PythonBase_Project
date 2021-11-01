FROM python:3.8.11-slim-buster
RUN pip3 install pipenv
WORKDIR /app
COPY Pipfile Pipfile.lock main.py /app/
RUN set -ex && pipenv install --system
EXPOSE 8000
CMD ["uvicorn", "--host=0.0.0.0", "main:app"]
