class SongInfo:
    def __init__(self):
        self.title = None
        self.duration = None
        self.download_link = None

    def fromYT(self, song_info):
        # self.id = song_info["id"]  # 'id': 'qKeJtTSCRiM'
        # self.thumbnails = song_info["thumbnails"]  # 'thumbnails': ['images', 'images']
        self.title = song_info["title"]  # 'title': 'ЗАМАЙ - ЗАМАЙ (ПРЕМЬЕРА ЗАМАЙ)'
        # self.long_desc = song_info["long_desc"]  # 'long_desc': None
        # self.channel = song_info["channel"]  # 'channel': 'ЗАМАЙ'
        self.duration = song_info["duration"]  # 'duration': '2:54'
        # self.views = song_info["views"]  # 'views': '175\xa0239 просмотров'
        # self.publish_time = song_info["publish_time"]  # 'publish_time': '7 месяцев назад'
        self.download_link = song_info["url_suffix"]  # 'url_suffix': '/watch?v=qKeJtTSCRiM'

    def fromVK(self, song_info):
        # self.artist = song_info["artist"]  # 'artist': '1.Kla$'
        self.duration = song_info["duration"]  # 'duration': 225
        # self.id = song_info["id"]  # 'id': 456430866
        # self.owner_id = song_info["owner_id"]  # 'owner_id': 474499307
        self.title = song_info["artist"] + " " + song_info["title"]  # 'title': 'Это Я'
        # self.track_covers = song_info["track_covers"]  # 'track_covers': ['images', 'images']
        self.download_link = song_info["url"]  # 'url': 'https://cfytr4.vkuseraudio.net/s/v1/ac/_jL5ad_sdf/index.m3u8'
