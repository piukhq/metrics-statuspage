FROM ghcr.io/binkhq/python:3.9

WORKDIR /app
ADD main.py .
ADD Pipfile .
ADD Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["linkerd-await", "--"]
