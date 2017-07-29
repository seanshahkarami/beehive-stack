#!/bin/sh

cd cassandra
docker build -t beehive-cassandra .
cd ..

cd nginx
docker build -t beehive-nginx .
cd ..

cd web
docker build -t beehive-web .
cd ..

cd rabbitmq
docker build -t beehive-rabbitmq .
cd ..
