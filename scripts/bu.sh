#!/bin/bash
mydir=${0%/*}
cd ${mydir}/..
docker build -t server . -f dockerfiles/server/Dockerfile
docker build -t saver . -f dockerfiles/saver/Dockerfile
docker build -t pose . -f dockerfiles/pose/Dockerfile
docker build -t feelings . -f dockerfiles/feelings/Dockerfile
docker build -t color . -f dockerfiles/color-image/Dockerfile
docker build -t depth . -f dockerfiles/depth-image/Dockerfile
docker build -t api . -f dockerfiles/api/Dockerfile
docker build -t gui . -f dockerfiles/gui/Dockerfile
docker run -d -p 5672:5672 rabbitmq
docker run -d -p 27017:27017 mongo
docker run --rm -d -ti -p 8000:8000 -p 5672:5672 -v /tmp/data:/data_dir server
docker run --rm -d -ti -p 5672:5672 -p 27017:27017 saver
docker run --rm -d -p 5672:5672 -ti pose
docker run --rm -d -p 5672:5672 -ti feelings
docker run --rm -d -ti -p 5672:5672 -v /tmp/data:/data_dir color
docker run --rm -d -ti -p 5672:5672 -v /tmp/data:/data_dir depth
docker run --rm -d -ti -p 5000:5000 -p 27017:27017 -v /tmp/data:/data_dir api
docker run --rm -d -ti -p 8080:8080 -v /tmp/data:/data_dir gui
