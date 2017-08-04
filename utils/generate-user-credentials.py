#!/usr/bin/env python3
import secrets
import json

usernames = [
    'loader',
    'publisher1',
    'publisher2',
    'publisher3',
    'publisher4',
    'publisher5',
    'worker1',
    'worker2',
    'worker3',
    'worker4',
    'worker5',
]

credentials = {}

for username in usernames:
    credentials[username] = {
        'password': secrets.token_urlsafe(32),
        'tags': '',
    }

with open('credentials.json', 'w') as f:
    json.dump(credentials, f)
