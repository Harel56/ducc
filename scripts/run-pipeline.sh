#!/bin/bash
mydir=${0%/*}
docker build -t server ${mydir}/../dockerfiles/serverDockerfile
docker build -t saver ${mydir}/../dockerfiles/saverDockerfile
docker build -t pose ${mydir}/../dockerfiles/poseDockerfile
docker build -t feelings ${mydir}/../dockerfiles/feelingsDockerfile
docker build -t color ${mydir}/../dockerfiles/colorDockerfile
docker build -t depth ${mydir}/../dockerfiles/depthDockerfile
docker build -t api ${mydir}/../dockerfiles/apiDockerfile
docker build -t gui ${mydir}/../dockerfiles/guiDockerfile
docker run -d -p 5672:5672 rabbitmq
docker run -d -p 27017:27017 mongo
docker run -d -ti -p 8000:8000 -p 5672:5672 -v /tmp/data:/data_dir server
docker run -d -ti -p 5672:5672 -p 27017:27017 saver
docker run -d -p 5672:5672 -ti pose
docker run -d -p 5672:5672 -ti feelings
docker run -d -ti -p 5672:5672 -v /tmp/data:/data_dir color
docker run -d -ti -p 5672:5672 -v /tmp/data:/data_dir depth
docker run -d -ti -p 5000:5000 -p 27017:27017 -v /tmp/data:/data_dir api
docker run -d -ti -p 8080:8080 -v /tmp/data:/data_dir gui