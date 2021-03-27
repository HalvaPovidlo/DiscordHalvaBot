import logging
import os
import random

import discord
import youtube_dl
from youtube_search import YoutubeSearch

"""
skip
play
loop
shuffle
radio

"""

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


class MusicPlayer:
    def __init__(self):
        self._playlist = []  # list of youtube song url_suffixes
        self._player = None  # VoiceClient

    def queue_song(self, song):
        self._playlist.append(song['url_suffix'])

    def shuffle(self):
        random.shuffle(self._playlist)

    async def _update_player(self, ctx):
        if ctx.guild.voice_client:
            self._player = ctx.guild.voice_client
        else:
            self._player = await ctx.author.voice.channel.connect()

    async def _is_request_correct(self, ctx) -> bool:
        if not ctx.author.voice.channel:
            await ctx.send("Please connect to a voice channel.")
            return False
        if self._player and ctx.author.voice.channel != self._player.channel:
            await ctx.send(":x2: You need to be in the same voice channel as HalvaBot to use this command")
            return False
        return True

    async def process_song_request(self, ctx, song_str):
        print(song_str)
        if not await self._is_request_correct(ctx):
            return

        await self._update_player(ctx)

        song_info = YoutubeSearch(song_str, max_results=1).to_dict()[0]
        self.queue_song(song_info)

        self.play_next_song(0)

    def play_next_song(self, stub):
        print("play_next_song")
        if not self._player or self._player.is_playing() or len(self._playlist) == 0:
            return

        stubfile = "stubname.mp3"
        if os.path.exists(stubfile):
            os.remove(stubfile)

        ydl_opts['outtmpl'] = stubfile
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/' + self._playlist.pop(0)])

        self._player.play(discord.FFmpegPCMAudio(stubfile), after=self.play_next_song)
