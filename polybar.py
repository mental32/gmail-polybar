#!/usr/bin/env python3
import os
import sys

assert sys.version_info[:2] >= 3.6, 'fatal: requires Python 3.6+'

import argparse
import time
import pathlib

from apiclient import discovery, errors
from oauth2client import client, file
from httplib2 import ServerNotFoundError

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix', default='GMAIL => ')
parser.add_argument('-d', '--delay', default=10)
args = parser.parse_args()

STD_DELAY = int(args.delay)
DIR = os.path.dirname(os.path.realpath(__file__))
_CREDENTAILS_PATH = os.path.join(DIR, 'credentials.json')

def main():
    _CREDENTIALS_STORAGE = file.Storage(_CREDENTAILS_PATH)
    _GMAIL = discovery.build('gmail', 'v1', credentials=_CREDENTIALS_STORAGE.get())
    _LABEL = _GMAIL.users().labels().get(userId='me', id='INBOX')

    delay = STD_DELAY

    while True:
        print(f'{args.prefix}N', flush=True)

        while pathlib.Path(_CREDENTAILS_PATH).is_file():
            try:
                print(f'{args.prefix}{_LABEL.execute()["messagesUnread"]}', flush=True)

            except (errors.HttpError, ServerNotFoundError, OSError) as error:
                print(f'{args.prefix}N', flush=True)

            except client.AccessTokenRefreshError:
                print(f'{args.prefix}error(revoked/expired credentials)', flush=True)

            time.sleep(delay)


if __name__ == '__main__':
    main()
