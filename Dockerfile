FROM ghcr.io/binkhq/python:3.9 as build

WORKDIR /src
ADD main.py Pipfile Pipfile.lock ./

ENTRYPOINT ["linkerd-await", "--"]
