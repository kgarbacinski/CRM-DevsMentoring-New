FROM openjdk:17-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add python3 && apk add py3-pip	&& apk add --update nodejs npm && pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install -r requirements.txt 

EXPOSE 8002
# copy project
COPY . /usr/src/app/