import pika
import ssl

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
    print(properties, body, flush=True)
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(process_message, queue='raw-data')
