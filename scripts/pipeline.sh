#!/bin/bash
docker run -d -p 27017:27017 mongo
docker run -d -p 5672:5672 rabbitmq
python -m ducc.parsers run-parser pose rabbitmq://localhost:5672/ &
python -m ducc.parsers run-parser feelings rabbitmq://localhost:5672/ &
python -m ducc.parsers run-parser color rabbitmq://localhost:5672/ &
python -m ducc.parsers run-parser depth rabbitmq://localhost:5672/ &
python -m ducc.saver run-saver mongodb://localhost:27017/ rabbitmq://localhost:5672/ &
python -m ducc.server rabbitmq://localhost:5672/ &
python -m ducc.api
