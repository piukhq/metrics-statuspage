FROM ghcr.io/binkhq/python:3.9 as build

WORKDIR /app
ADD main.py .
ADD Pipfile .
ADD Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["python3", "main.py"]
