import json

from domain import secretConfig
from music.stats.database import Database
from music.stats.google_sheets_api import GoogleSheets
from music.stats.song import Song, SongJsonEncoder, SongJsonDecoder


class JSONDatabase(Database):
    def __init__(self, filename):
        self.filename = filename

    def read_data(self):
        with open(self.filename, 'r') as read_file:
            data = json.load(read_file, cls=SongJsonDecoder)
            return data

    def write_data(self, data):
        if secretConfig.discord_settings['debug']:
            return
        with open(self.filename, 'w') as write_file:
            json.dump(data, write_file, cls=SongJsonEncoder)


def main():
    gs = GoogleSheets()
    songs: {str: Song} = gs.read_data()
    js = JSONDatabase("music_stats.json")
    js.write_data(songs)
    print(js.read_data())


if __name__ == '__main__':
    main()
