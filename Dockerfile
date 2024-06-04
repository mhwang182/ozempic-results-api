# syntax=docker/dockerfile:1

#base image
FROM python:3.8-slim-buster 
#
WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ARG mongo_uri
ENV MONGO_URI $mongo_uri

ARG database_name
ENV DATABASE_NAME $database_name

ARG bucket_name
ENV BUCKET_NAME $bucket_name

ARG s3_access_key_id
ENV S3_ACCESS_KEY_ID $s3_access_key_id

ARG s3_secret_access_key
ENV S3_SECRET_ACCESS_KEY $s3_secret_access_key

ARG s3_endpoint_url
ENV S3_ENDPOINT_URL $s3_endpoint_url

ARG api_key
ENV API_KEY $api_key

CMD [ "python3", "app.py" ]

EXPOSE 8080