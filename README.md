# Beehive Stack

This is an experiment in using the Docker stack features to get a set of
beehive services running. (See waggle project for more info...)

## Prerequisites

### Secrets

You'll need to define a few secrets to successfully run the stack.

```sh
docker secret create cacert /path/to/cacert.pem

docker secret create nginx_cert /path/to/nginx_cert.pem
docker secret create nginx_key /path/to/nginx_key.pem

docker secret create rabbitmq_cert /path/to/rabbitmq_cert.pem
docker secret create rabbitmq_key /path/to/rabbitmq_key.pem

docker secret create loader_cert /path/to/loader_cert.pem
docker secret create loader_key /path/to/loader_key.pem
```

## Deploying

First, docker must be running in swarm mode. The simplest way to set this up is:

```sh
docker swarm init
```

Now, you'll want to deploy the beehive stack.

```sh
docker stack deploy -c development.yml beehive
```
