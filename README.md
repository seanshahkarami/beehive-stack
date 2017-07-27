# Beehive Stack

This is an experiment in using the Docker stack features to get a set of
beehive services running. (See waggle project for more info...)

## Deploying

First, docker must be running in swarm mode. The simplest way to set this up is:

```sh
docker swarm init
```

Now, you'll want to deploy the beehive stack.

```sh
docker stack deploy -c docker-compose.yml beehive
```
