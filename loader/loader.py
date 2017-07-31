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
    created_at = columns.DateTime(primary_key=True)
    plugin_id = columns.Text(primary_key=True)
    topic = columns.Text()
    data = columns.Blob()


class SensorDataLog(Model):

    __options__ = {
        'default_time_to_live': 60,
    }

    node_id = columns.Text(partition_key=True)
    created_at = columns.DateTime(primary_key=True)
    plugin_id = columns.Text(primary_key=True)
    topic = columns.Text()
    data = columns.Blob()


connection.setup(['cassandra'], 'waggle')
create_keyspace_simple('waggle', replication_factor=3)
sync_table(SensorData)
sync_table(SensorDataLog)


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
    node_id = 'testnode'
    timestamp = datetime.now()

    SensorData.create(
        node_id=node_id,
        date=timestamp.date(),
        created_at=datetime.now(),
        plugin_id='testplugin:0.1',
        topic='test_topic',
        data=body,
    )

    SensorDataLog.create(
        node_id=node_id,
        created_at=datetime.now(),
        plugin_id='testplugin:0.1',
        topic='test_topic',
        data=body,
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(process_message, queue='raw-data')
channel.start_consuming()
