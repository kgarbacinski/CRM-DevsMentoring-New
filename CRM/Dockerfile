FROM python:3.9.5-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#install packages for Pillow
RUN apk add zlib-dev jpeg-dev gcc musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

COPY . /usr/src/app/