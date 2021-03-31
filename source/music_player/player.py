import os
import random

import discord
import youtube_dl
from youtube_search import YoutubeSearch

import music_player.player_messages as pm
from music_stats.music_manager import MusicManager

"""
skip
play
loop
shuffle
radio

"""

stubfile = "stubname.mp3"

ydl_opts = {
    'outtmpl': stubfile,
    'quiet': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


def is_longer_than_max(song_duration: str) -> bool:
    smh = song_duration.rsplit(":")
    max_minutes = 20
    if len(smh) > 1:
        return int(smh[-2]) > max_minutes - 1
    return False


class MusicPlayer:
    def __init__(self, manager: MusicManager):
        self.playlist = []  # list of youtube song url_suffixes
        self.player = None  # VoiceClient
        self.is_loop = False
        self.is_radio = False
        self.manager = manager

    def shuffle(self):
        random.shuffle(self.playlist)

    def skip(self):
        self.player.stop()

    def loop(self):
        self.is_loop = not self.is_loop

    async def enable_radio(self, ctx):
        self.is_radio = not self.is_radio
        if self.is_radio:
            await ctx.send(pm.RADIO_ENABLED)
            if self.player:
                if not self.player.is_playing:
                    print("starting")
                    await self.process_song_request(ctx, self.manager.radio_song())
            else:
                await self.process_song_request(ctx, self.manager.radio_song())
        else:
            await ctx.send(pm.RADIO_DISABLED)

    def stop(self):
        self.is_loop = False
        self.is_radio = False
        self.playlist = []
        if self.player:
            self.player.stop()

    def pause(self):
        if self.player:
            self.player.pause()

    def resume(self):
        self.player.resume()

    async def disconnect(self):
        self.stop()
        if self.player and self.player.is_connected():
            await self.player.disconnect()

    async def process_song_request(self, ctx, song_str):
        print(song_str)
        if not await self._is_request_correct(ctx):
            return

        await self._update_player(ctx)

        await ctx.send(f"{pm.SEARCHING} {song_str}")
        if self._find_and_queue_song(song_str):
            if not self.player.is_playing():
                self._play_next_song()
            return
        await ctx.send(pm.NO_MATCH)

    def _find_and_queue_song(self, name) -> bool:
        print("find_and_queue_song", name)
        song = self.find_song(name)
        print(song)
        if song:
            self.playlist.append(song['url_suffix'])
            return True
        return False

    async def _update_player(self, ctx):
        if ctx.guild.voice_client:
            self.player = ctx.guild.voice_client
        else:
            self.player = await ctx.author.voice.channel.connect()

    async def _is_request_correct(self, ctx) -> bool:
        if not ctx.author.voice.channel:
            await ctx.send("Please connect to a voice channel.")
            return False
        if self.player and self.player.is_connected() and ctx.author.voice.channel != self.player.channel:
            await ctx.send(":x2: You need to be in the same voice channel as HalvaBot to use this command")
            return False
        return True

    def _play_next_song(self):
        print("play_next_song", self.playlist)
        if not self.player:
            return
        self.player.stop()
        self._start_playlist_radio()

    def _on_song_stops(self, error):
        if error:
            print(error)

        if self.is_loop:
            self.player.play(discord.FFmpegPCMAudio(stubfile), after=self._on_song_stops)
            return

        self._start_playlist_radio()

    def _start_playlist_radio(self):
        if len(self.playlist) == 0:
            if self.is_radio:
                song = self.find_song(self.manager.radio_song())
                if song:
                    print(song)
                    self._download_than_play(song['url_suffix'])
        else:
            print(self.playlist)
            self._download_than_play(self.playlist.pop(0))

    @staticmethod
    def find_song(name):
        song_info = YoutubeSearch(name, max_results=1).to_dict()
        print("YoutubeSearch(self.manager.radio_song()")

        if song_info[0]['url_suffix']:
            if is_longer_than_max(song_info[0]['duration']):
                return None
            return song_info[0]
        else:
            return None

    def _download_than_play(self, name):
        while os.path.exists(stubfile):
            try:
                os.remove(stubfile)
            finally:
                pass

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("youtube_dl.YoutubeDL(ydl_opts) as ydl")
            ydl.download(['https://www.youtube.com/' + name])
            self.player.play(discord.FFmpegPCMAudio(stubfile), after=self._on_song_stops)
