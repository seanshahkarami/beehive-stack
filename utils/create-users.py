#!/usr/bin/env python3
from configparser import ConfigParser
import requests
import json


def list_accounts():
    config = ConfigParser()
    config.read('credentials')

    for profile, section in config.items():
        try:
            username = section['beehive_username']
            password = section['beehive_password']
            yield username, password
        except KeyError:
            continue


def create_user(username, credentials):
    auth = ('admin', 'admin')
    headers = {'content-type': 'application/json'}

    r = requests.put(
        url='https://localhost:15671/api/users/{}'.format(username),
        auth=auth,
        headers=headers,
        verify=False,
        data=json.dumps(credentials),
    )

    assert r.status_code in [201, 204]

    data = {
        'configure': '.*',
        'read': '.*',
        'write': '.*',
    }

    r = requests.put(
        url='https://localhost:15671/api/permissions/%2f/{}'.format(username),
        auth=auth,
        headers=headers,
        verify=False,
        data=json.dumps(data),
    )


for username, password in list_accounts():
    print(username, password)
# for username, credentials in load_credentials().items():
#     print('creating user {}'.format(username))
#     create_user(username, credentials)
