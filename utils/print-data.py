#!/usr/bin/env python3
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model


class SensorData(Model):

    node_id = columns.Text(partition_key=True)
    date = columns.Date(partition_key=True)
    created_at = columns.DateTime(primary_key=True)
    plugin_id = columns.Text(primary_key=True)
    topic = columns.Text()
    data = columns.Blob()


connection.setup(['localhost'], 'waggle')

q = SensorData.objects()

for r in q:
    print(r.node_id, r.created_at, r.data)

print(q.count())
