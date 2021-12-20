import os

import discord

from music.song_info import SongInfo


class Searcher(discord.PCMVolumeTransformer):
    def __init__(self, source, *, song_info: SongInfo, filename, volume=0.5):
        super().__init__(source, volume)

        self.song_info = song_info

        self.filename = filename
        self.title = song_info.title
        self.url = song_info.download_link

    @classmethod
    async def download(cls, song_info: SongInfo, *, loop=None, stream=False):
        """Returns: cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)"""
        pass

    def find(self, query: str) -> SongInfo:
        """Returns song's data"""
        pass

    def delete(self):
        print("Delete", self.filename)
        if os.path.exists(self.filename):
            os.remove(self.filename)
        else:
            print("The file does not exist")

    def __del__(self):
        self.delete()
        super().__del__()
