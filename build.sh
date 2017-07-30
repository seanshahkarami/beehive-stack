#!/bin/sh

build_image() {
  cd $1
  docker build -t beehive-$1 .
  cd ..
}

build_image nginx
build_image rabbitmq
build_image web
