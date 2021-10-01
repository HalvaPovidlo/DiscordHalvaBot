import asyncio
import os

import discord
from youtube_search import YoutubeSearch

from music_player.Searcher.searcher import Searcher
import youtube_dl


# Suppress noise about console usage from errors
from utilities import logerr, loginfo

youtube_dl.utils.bug_reports_message = lambda: ''

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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(Searcher):
    def __init__(self, *, source, data, filename, volume=0.5):
        if source:
            super().__init__(source, data=data, filename=filename, volume=volume)
        else:
            super().__init__(discord.FFmpegPCMAudio(stubfile, **ffmpeg_options),
                             data=data, volume=volume, filename=filename)

    @classmethod
    async def from_url(cls, url_suffix, *, loop=None, stream=False) -> Searcher:
        """Overrides Searcher.from_url"""
        to_download = 'https://www.youtube.com' + url_suffix
        song_id = url_suffix.split("=", 1)[1]

        song_filename = find_free_name(song_id + ".mp3")

        print(to_download)
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(to_download, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        os.rename(filename, song_filename)
        return cls(source=discord.FFmpegPCMAudio(song_filename, **ffmpeg_options), data=data, filename=song_filename)

    def find(self, query: str):
        return find_song(query)


def find_free_name(name: str):
    i = 0
    new_name = name
    while os.path.exists(new_name):
        new_name = str(i) + name
        i += 1
    return new_name


def find_song(name: str):
    print("Finding", name)
    try:
        song_info = YoutubeSearch(name, max_results=1).to_dict()
        print("Found", song_info[0]['title'])
        loginfo(f"Found {song_info[0]['title']} : {song_info[0]['duration']}")
        return song_info[0]

    except Exception:
        logerr(f"YoutubeSearch({name}, max_results=1)")
        return None
