#!/usr/bin/env python3
import os
import sys

assert sys.version_info[:2] >= (3, 5), 'fatal: requires Python 3.5+'

import argparse
import time
import pathlib
import socket

from apiclient import discovery, errors
from apiclient.errors import HttpError
from oauth2client import client, file
from httplib2 import ServerNotFoundError

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix', default='GMAIL({count})')
parser.add_argument('-d', '--delay', default=5)
args = parser.parse_args()

STD_DELAY = int(args.delay)
DIR = os.path.dirname(os.path.realpath(__file__))
_CREDENTAILS_PATH = os.path.join(DIR, 'credentials.json')

def wait_for_connection():
    sock = socket.socket()

    while True:
        try:
            sock.connect(('8.8.8.8', 53))
            return sock.close()
        except OSError:
            print('Gmail::Failed to connect.', flush=True)
            time.sleep(1)
            continue

def main(delay=None):
    delay = delay or STD_DELAY

    wait_for_connection()

    _CREDENTIALS_STORAGE = file.Storage(_CREDENTAILS_PATH)
    _GMAIL = discovery.build('gmail', 'v1', credentials=_CREDENTIALS_STORAGE.get())
    _LABEL = _GMAIL.users().labels().get(userId='me', id='INBOX')

    while True:
        try:
            while pathlib.Path(_CREDENTAILS_PATH).is_file():
                print(args.prefix.format(count=_LABEL.execute()["messagesUnread"]), flush=True)
                time.sleep(delay)

        except client.AccessTokenRefreshError:
            print('Gmail::revoked/expired credentials', flush=True)
            break

        except (HttpError, ServerNotFoundError, OSError):
            pass

if __name__ == '__main__':
    main()
