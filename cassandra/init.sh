#/bin/sh

setup() {
  while true; do
    sleep 5
    cqlsh -f /init.cql || continue
    break
  done
}

setup &
cassandra -f -R $@
