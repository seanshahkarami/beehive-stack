#!/bin/sh

push_image() {
  docker tag beehive-$1 seanshahkarami/beehive-$1 && docker push seanshahkarami/beehive-$1
}

push_image cassandra
push_image nginx
push_image rabbitmq
push_image web
