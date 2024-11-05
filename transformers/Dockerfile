# syntax=docker/dockerfile:1
FROM python:3.11.3-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app


RUN apt-get update && \
    apt-get install -y --no-install-recommends curl


# install app dependencies
COPY  ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN addgroup --system appuser && adduser --system --group appuser
USER appuser

COPY . /usr/src/app/

# final configuration
EXPOSE 8000