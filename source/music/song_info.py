class SongInfo:
    def __init__(self, song_info):
        self.id = song_info["id"]  # 'id': 'qKeJtTSCRiM'
        self.thumbnails = song_info["thumbnails"]  # 'thumbnails': ['images', 'images']
        self.title = song_info["title"]  # 'title': 'ЗАМАЙ - ЗАМАЙ (ПРЕМЬЕРА ЗАМАЙ)'
        self.long_desc = song_info["long_desc"]  # 'long_desc': None
        self.channel = song_info["channel"]  # 'channel': 'ЗАМАЙ'
        self.duration = song_info["duration"]  # 'duration': '2:54'
        self.views = song_info["views"]  # 'views': '175\xa0239 просмотров'
        self.publish_time = song_info["publish_time"]  # 'publish_time': '7 месяцев назад'
        self.url_suffix = song_info["url_suffix"]  # 'url_suffix': '/watch?v=qKeJtTSCRiM'
