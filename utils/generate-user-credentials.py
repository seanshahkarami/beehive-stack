#!/usr/bin/env python3
import secrets

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

for username in usernames:
    password = secrets.token_urlsafe(32)

    print('[{}]'.format(username))
    print('beehive_username={}'.format(username))
    print('beehive_password={}'.format(password))
    print()
