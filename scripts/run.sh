#!/bin/bash
mydir=${0%/*}
cd ${mydir}/..
docker run -d -p 27017:27017 --name db mongo
docker run --rm -d -p 5672:5672 --name rabbit rabbitmq
sleep 10
docker run --rm -d --network host -v data:/data_dir --name waiter server
sleep 5
docker run --rm -d --network host --name arch saver
sleep 5
docker run --rm -d --network host --name yoga pose
docker run --rm -d --network host --name drama feelings
docker run --rm -d --network host --volumes-from waiter --name painter color
docker run --rm -d --network host --volumes-from waiter --name digger depth
docker run --rm -d --network host -v /tmp/data:/data_dir api
docker run --rm -d --network host -v data:/data_dir --name web gui
