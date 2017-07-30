#/bin/sh

setup() {
  sleep 30
  cqlsh -f /init.cql
}

# sed -i "s/CONTAINER_IP_ADDRESS/$(hostname --ip-address)/" /etc/cassandra/cassandra.yaml

setup &
cassandra -f -R $@
