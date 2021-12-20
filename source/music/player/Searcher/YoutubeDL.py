import asyncio
import os

import discord
from youtube_search import YoutubeSearch
import yt_dlp

from music.player.Searcher.searcher import Searcher
from music.song_info import SongInfo
from domain.utilities import logerr, loginfo, find_free_name

stubfile = "stubname.mp3"

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl':  '%(extractor)s-%(id)s-%(title)s.mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(Searcher):
    def __init__(self, *, source, song_info, filename, volume=0.5):
        if source:
            super().__init__(source, song_info=song_info, filename=filename, volume=volume)
        else:
            super().__init__(discord.FFmpegPCMAudio(stubfile, **ffmpeg_options),
                             song_info=song_info, volume=volume, filename=filename)

    @classmethod
    async def download(cls, song_info: SongInfo, *, loop=None, stream=False) -> Searcher:
        """Overrides Searcher.download"""
        to_download = 'https://www.youtube.com' + song_info.download_link
        song_id = song_info.download_link.split("=", 1)[1]

        song_filename = find_free_name(song_id + ".mp3")

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(to_download, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        os.rename(filename, song_filename)
        return cls(source=discord.FFmpegPCMAudio(song_filename, **ffmpeg_options), song_info=song_info
                   , filename=song_filename)

    def find(self, query: str) -> SongInfo:
        try:
            song_info: SongInfo = SongInfo()
            song_info.fromYT(YoutubeSearch(query, max_results=1).to_dict()[0])
            print("Found", song_info.title)
            loginfo(f"Found {song_info.title} : {song_info.duration}")
            return song_info
        except Exception as e:
            logerr(f"YoutubeSearch({query}, max_results=1) {e}")
            return None
