from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.management import create_keyspace_simple
from cassandra.cqlengine.models import Model
from datetime import datetime
import pika
import ssl


class SensorData(Model):

    node_id = columns.Text(partition_key=True)
    date = columns.Date(partition_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime()
    plugin_id = columns.Text(primary_key=True)
    topic = columns.Text()
    data = columns.Blob()


class SensorDataLog(Model):

    __options__ = {
        'default_time_to_live': 60,
    }

    node_id = columns.Text(partition_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime()
    plugin_id = columns.Text(primary_key=True)
    topic = columns.Text()
    data = columns.Blob()


def process_message(ch, method, properties, body):
    user_id = properties.user_id
    received_at = datetime.utcnow()
    created_at = datetime.utcfromtimestamp(properties.timestamp // 1000)
    plugin_id = method.routing_key
    topic = properties.type

    # idempotence of database inserts combined with message acknowledgement
    # ensures that the database tables will be consistent before continuing

    SensorData.create(
        node_id=user_id,
        date=received_at.date(),
        created_at=created_at,
        received_at=received_at,
        plugin_id=plugin_id,
        topic=topic,
        data=body,
    )

    SensorDataLog.create(
        node_id=user_id,
        created_at=created_at,
        received_at=received_at,
        plugin_id=plugin_id,
        topic=topic,
        data=body,
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    # setup cassandra connection and models
    connection.setup(['cassandra'], 'waggle')
    create_keyspace_simple('waggle', replication_factor=3)
    sync_table(SensorData)
    sync_table(SensorDataLog)

    # connect to message broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq',
        port=5671,
        credentials=pika.PlainCredentials(
            username='loader',
            password='uvZVGPT8Hknd6s96Xn_J7f5LTuC4Nz0st-iuxJeeGWk',
        ),
        connection_attempts=5,
        retry_delay=5.0,
        ssl=True,
        ssl_options={
            'cert_reqs': ssl.CERT_REQUIRED,
            'ca_certs': '/run/secrets/cacert',
        }
    ))

    # get channel and start processing messages
    channel = connection.channel()
    channel.basic_consume(process_message, queue='raw-data')
    channel.start_consuming()
