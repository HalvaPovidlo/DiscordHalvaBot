import pickle
import os.path
import sys
from enum import Enum
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from music.stats.database import Database
from music.stats.song import Song
from domain.secretConfig import secret_config as sc
from domain.utilities import loginfo

DEBUG_MODE = sc.discord()['debug']


class Columns(Enum):
    NAME = 0
    LINK = 1
    COUNTER = 2
    LAST_PLAY_DATE = 3


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = sc.gsheets()['id']
ALL_DATA_RANGE = 'A2:D9000'


class GoogleSheets(Database):
    def __init__(self):
        self.service = get_service()

    def read_data(self):
        data = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ALL_DATA_RANGE).execute()
        data = data.get('values', [])
        result = {}
        for i in data:
            result[i[Columns.NAME.value]] = Song(i[Columns.NAME.value], i[Columns.LINK.value],
                                                 int(i[Columns.COUNTER.value]), i[Columns.LAST_PLAY_DATE.value])

        return result

    def write_data(self, data):
        if DEBUG_MODE:
            return

        to_write = []
        for song in data.values():
            list_song = [None] * (Columns.LAST_PLAY_DATE.value + 1)
            list_song[Columns.NAME.value] = song.title
            list_song[Columns.LINK.value] = song.url
            list_song[Columns.COUNTER.value] = song.counter
            list_song[Columns.LAST_PLAY_DATE.value] = song.date
            to_write.append(list_song)

        to_write.sort(key=lambda x: int(x[Columns.COUNTER.value]), reverse=True)
        data = [
            {
                'range': ALL_DATA_RANGE,
                'values': to_write
            },
        ]
        body = {
            'valueInputOption': 'RAW',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID, body=body).execute()

        loginfo('{0} cells updated.'.format(result.get('totalUpdatedCells')))
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


def get_service():
    creds = None
    file_dir = os.path.dirname(sys.modules['__main__'].__file__)
    creds_path = os.path.join(file_dir, 'credentials.json')
    token_path = os.path.join(file_dir, 'token.pickle')
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def main():
    gs = GoogleSheets()
    songs: {str: Song} = gs.read_data()
    print(songs.keys())


if __name__ == '__main__':
    main()
