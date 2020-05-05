#!/bin/bash
mydir=${0%/*}
cd ${mydir}/..
docker run -d -p 27017:27017 --name db mongo
docker run -d -p 5672:5672 --name rabbit rabbitmq
sleep 5
. .env/bin/activate
python -m ducc.parsers run-parser pose rabbitmq://localhost:5672/ &
python -m ducc.parsers run-parser feelings rabbitmq://localhost:5672/ &
python -m ducc.parsers run-parser color rabbitmq://localhost:5672/ &
python -m ducc.parsers run-parser depth rabbitmq://localhost:5672/ &
python -m ducc.saver run-saver mongodb://localhost:27017/ rabbitmq://localhost:5672/ &
python -m ducc.server run-server rabbitmq://localhost:5672/ &
