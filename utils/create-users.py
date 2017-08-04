#!/usr/bin/env python3
import requests
import json


def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)


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


for username, credentials in load_credentials().items():
    print('creating user {}'.format(username))
    create_user(username, credentials)
