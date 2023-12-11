# FROM python:3.10-alpine
FROM python:3.10-slim

RUN pip install --upgrade pip

# Install system dependencies
# RUN apk update && apk add python3-dev \
#                           gcc \
#                           g++ \
#                           libc-dev \
#                           libffi-dev \
#                           cmake

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# install prerequisites
RUN pip install poetry==1.5.1

# Install dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# install dependencies
WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock

RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the application
COPY ./api /code/api

COPY ./webapp /code/webapp