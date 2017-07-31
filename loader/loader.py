from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.management import create_keyspace_simple
from cassandra.cqlengine.models import Model
import pika
import ssl
from datetime import datetime


class SensorData(Model):

    node_id = columns.Text(partition_key=True)
    date = columns.Date(partition_key=True)
    plugin_id = columns.Text(primary_key=True)
    created_at = columns.DateTime(primary_key=True)
    topic = columns.Text()
    data = columns.Blob()


connection.setup(['127.0.0.1'], 'waggle')
create_keyspace_simple('waggle', replication_factor=3)
sync_table(SensorData)


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    port=5671,
    credentials=pika.PlainCredentials(
        username='tester',
        password='tester',
    ),
    connection_attempts=5,
    retry_delay=5.0,
    ssl=True,
    ssl_options={
        'cert_reqs': ssl.CERT_REQUIRED,
        'ca_certs': '/run/secrets/cacert',
        'certfile': '/run/secrets/loader_cert',
        'keyfile': '/run/secrets/loader_key',
    }
))

channel = connection.channel()


def process_message(ch, method, properties, body):
    timestamp = datetime.now()

    SensorData.create(
        node_id='testnode',
        date=timestamp.date(),
        plugin_id='testplugin:0.1',
        created_at=datetime.now(),
        data=body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(process_message, queue='raw-data')
channel.start_consuming()
