#alpine image that contain python3.5
FROM python:3.5-alpine

#defining the directory to work in
WORKDIR /app

#copying the requirements.txt file to the work directory
COPY requirements.txt .

# install some system deps in a virtual enviroment named .build-deps

#installing pip dependencies in the same layer
RUN apk add --no-cache --virtual .build-deps \
    build-base openssl-dev pkgconfig libffi-dev \
    cups-dev jpeg-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

#coping rest of the code
COPY . /app

#Exposing the needed port
EXPOSE 80

#running command on entry point
CMD python ./server.py