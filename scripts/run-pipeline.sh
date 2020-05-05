#!/bin/bash
mydir=${0%/*}
cd ${mydir}/..
docker run --rm -d -p 5672:5672 --name qu rabbitmq
docker run -d --network host --name db mongo
docker build -t server . -f dockerfiles/server/Dockerfile
docker run --rm -d --network host -v data:/data_dir --name waiter server
docker build -t saver . -f dockerfiles/saver/Dockerfile
docker run --rm -d --network host --name arch saver
docker build -t pose . -f dockerfiles/pose/Dockerfile
docker run --rm -d --network host --name yoga pose
docker build -t feelings . -f dockerfiles/feelings/Dockerfile
docker run --rm -d --network host --name drama feelings
docker build -t color . -f dockerfiles/color-image/Dockerfile
docker run --rm -d --network host --volumes-from waiter --name painter color
docker build -t depth . -f dockerfiles/depth-image/Dockerfile
docker run --rm -d --network host --volumes-from waiter --name digger depth
docker build -t api . -f dockerfiles/api/Dockerfile
docker run --rm -d --network host --volumes-from waiter api
docker build -t gui . -f dockerfiles/gui/Dockerfile
docker run --rm -d -ti --network host --volumes-from waiter --name web gui

