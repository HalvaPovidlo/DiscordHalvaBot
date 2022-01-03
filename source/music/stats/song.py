import json


class Song:
    def __init__(self, title, url, counter, date):
        self.title: str = title
        self.url: str = url
        self.counter: int = counter
        self.date: str = date  # date.today().strftime("%d/%m/%Y")


class SongJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class SongJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if 'title' in dct:
            return Song(dct['title'], dct['url'], dct['counter'], dct['date'])
        return dct
