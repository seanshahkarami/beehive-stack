#!/usr/bin/env python3
import waggle.credentials
import pika
import ssl
import time
from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser(description='Runs test publisher')
parser.add_argument('-p', '--profile', default='publisher1', help='credentials profile to use')
args = parser.parse_args()

credentials = waggle.credentials.load(args.profile)
username = credentials['beehive_username']
password = credentials['beehive_password']

print('publishing using profile {}'.format(args.profile))

parameters = pika.ConnectionParameters(
    host='localhost',
    port=5671,
    credentials=pika.PlainCredentials(
        username=username,
        password=password,
    ),
    connection_attempts=5,
    retry_delay=5.0,
    socket_timeout=10.0,
    ssl=True,
    ssl_options={
        'cert_reqs': ssl.CERT_REQUIRED,
        'ca_certs': '/Users/Sean/github/testca/certs/ca.pem',
    }
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

print('connected')

while True:
    timestr = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    utctimestamp = int(1000 * datetime.now().timestamp())

    channel.basic_publish(
        properties=pika.BasicProperties(
            timestamp=utctimestamp,
            user_id=username,
        ),
        exchange='data-pipeline-in',
        routing_key='hello:1',
        body=timestr.encode())

    print('published')

    time.sleep(1)
