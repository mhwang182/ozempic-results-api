# syntax=docker/dockerfile:1

#base image
FROM python:3.8-slim-buster 
#
WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ]

EXPOSE 8080