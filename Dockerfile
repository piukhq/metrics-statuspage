FROM ghcr.io/binkhq/python:3.10

WORKDIR /app
COPY main.py settings.py Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["linkerd-await", "--shutdown", "--"]
