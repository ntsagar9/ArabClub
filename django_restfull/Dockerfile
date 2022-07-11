FROM python:3.10.5-slim-buster
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update -y
RUN apt install gcc libpq-dev python3-dev  -y
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./.env .
RUN pip install -r requirements.txt
COPY . .
