#!/usr/bin/env python

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None

    path = os.path.dirname(os.path.realpath(__file__))
    cfile = path + '/credentials.json'
    tfile = path + '/token.json'

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tfile):
        creds = Credentials.from_authorized_user_file(tfile, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cfile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tfile, 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Get Labels
        #results = service.users().labels().list(userId='me').execute()
        #labels = results.get('labels', [])
        #if not labels:
        #    print('No labels found.')
        #    return
        #print('Labels:')
        #for label in labels:
        #    print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    try:
        response = service.users().threads().list(
            userId='me', q='label:TRASH').execute()
        threads = []
        if 'threads' in response:
            threads.extend(response['threads'])
            for thread in threads:
                try:
                    items = service.users().threads().get(
                        userId='me', id=thread['id']).execute()

                    for item in items['messages']:
                        #print('Deleting message: %s' % item['id'])
                        service.users().messages().delete(
                            userId='me', id=item['id']).execute()

                except HttpError as error:
                    print('An error occurred: %s' % error)

    except HttpError as error:
        print('An error occurred: %s' % error)



if __name__ == '__main__':
    main()
