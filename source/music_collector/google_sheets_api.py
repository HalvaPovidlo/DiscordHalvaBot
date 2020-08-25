from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from secretConfig import gsheets_settings
from enum import Enum


class Columns(Enum):
    NAME = 0
    LINK = 1
    COUNTER = 2


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = gsheets_settings['id']
ALL_DATA_RANGE = 'A2:C100'


def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


service = get_service()


def read_all_data():
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ALL_DATA_RANGE).execute()
    return result.get('values', [])


def write_all_data(data):
    data = [
        {
            'range': ALL_DATA_RANGE,
            'values': data
        },
    ]
    body = {
        'valueInputOption': 'RAW',
        'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


def main():
    values = read_all_data()
    print(values)
    values.sort(key=lambda x: int(x[Columns.COUNTER.value]))
    print(values)
    write_all_data(values)


if __name__ == '__main__':
    main()
