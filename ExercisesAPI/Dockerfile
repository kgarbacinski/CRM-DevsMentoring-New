FROM python:3.9.5-alpine


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
EXPOSE 8002

COPY . /usr/src/app/