import json
from os import path

from domain import secretConfig
from music.stats.database import Database
from music.stats.google_sheets_api import GoogleSheets
from music.stats.song import Song, SongJsonEncoder, SongJsonDecoder


class JSONDatabase(Database):
    def __init__(self, filename):
        self.filename = filename

    def read_data(self):
        if not path.exists(self.filename):
            with open(self.filename, 'w') as write_file:
                json.dump("", write_file)

        with open(self.filename, 'r') as read_file:
            data = json.load(read_file, cls=SongJsonDecoder)
            if len(data) == 0:
                return {}
            return data

    def write_data(self, data):
        if secretConfig.secret_config.discord()['debug']:
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
