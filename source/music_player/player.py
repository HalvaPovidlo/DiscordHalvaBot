import logging
import os
import random

from discord import VoiceClient
from discord import FFmpegPCMAudio
from discord.ext.commands import Context
import youtube_dl
from youtube_search import YoutubeSearch

from utilities import number_to_emojis
import music_player.player_messages as pm
from music_stats.music_manager import MusicManager

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
        self.player: VoiceClient = None
        self.is_loop: bool = False
        self.is_radio: bool = False
        self.manager: MusicManager = manager
        self.current_song: str = ""

    async def shuffle(self, ctx: Context):
        await ctx.send(pm.SHUFFLE)
        random.shuffle(self.playlist)

    async def skip(self, ctx: Context):
        if self.player:
            await ctx.send(pm.SKIPPED)
            self.player.stop()

    async def loop(self, ctx: Context):
        self.is_loop = not self.is_loop
        if self.is_loop:
            await ctx.send(pm.LOOP_ENABLED)
        else:
            await ctx.send(pm.LOOP_DISABLED)

    async def enable_radio(self, ctx: Context):
        self.is_radio = not self.is_radio

        if not self.is_radio:
            await ctx.send(pm.RADIO_DISABLED)
            return

        if not await self._is_request_correct(ctx):
            return

        await self._update_player(ctx)
        self._start_playlist_radio()
        await ctx.send(pm.RADIO_ENABLED)

    async def stop(self, ctx: Context):
        self.is_loop = False
        self.is_radio = False
        self.playlist = []
        if self.player:
            await ctx.send(pm.STOP)
            self.player.stop()

    async def pause(self, ctx: Context):
        if self.player:
            await ctx.send(pm.PAUSE)
            self.player.pause()

    async def resume(self, ctx: Context):
        if self.player:
            await ctx.send(pm.RESUME)
            self.player.resume()

    async def current(self, ctx: Context):
        if self.current_song != "":
            await ctx.send(f"{pm.CURRENT} {self.current_song}")
        else:
            await ctx.send(pm.NO_CURRENT)

    async def disconnect(self, ctx: Context):
        await self.stop(ctx)
        if self.player and self.player.is_connected():
            await self.player.disconnect()

    async def process_song_request(self, ctx: Context, song_str: str):
        print(song_str)
        if not await self._is_request_correct(ctx):
            return

        await self._update_player(ctx)

        await ctx.send(f"{pm.SEARCHING} {song_str}")
        song = self._find_song(song_str)
        if song:
            self.playlist.append(song['url_suffix'])
            counter = self.manager.collect_song_from_player(song)
            await ctx.send(f"{pm.START_PLAYING.format(song_name=song['title'])}   {number_to_emojis(counter)}")

            self._start_playlist_radio()
        else:
            await ctx.send(pm.NO_MATCH)

    async def _update_player(self, ctx: Context):
        print("player updated")
        if ctx.guild.voice_client:
            self.player = ctx.guild.voice_client
        else:
            self.player = await ctx.author.voice.channel.connect()

    async def _is_request_correct(self, ctx: Context) -> bool:
        if not ctx.author.voice.channel:
            await ctx.send(pm.CONNECT_TO_CHANNEL)
            return False
        if self.player and self.player.is_connected() and ctx.author.voice.channel != self.player.channel:
            await ctx.send(pm.WRONG_CHANNEL)
            return False
        return True

    def _on_song_stops(self, error):
        self.current_song = ""
        if error:
            logging.error(error)
            print(error)

        if self.is_loop:
            self.player.play(FFmpegPCMAudio(stubfile), after=self._on_song_stops)
            return

        self._start_playlist_radio()

    def _start_playlist_radio(self):
        print("start_playlist_radio")
        if self.player.is_playing():
            return

        if len(self.playlist) == 0:
            if self.is_radio:
                song = self._find_song(self.manager.radio_song())
                if song:
                    print(song)
                    self._download_then_play(song['url_suffix'])
                else:
                    self._start_playlist_radio()
        else:
            print(self.playlist)
            self._download_then_play(self.playlist.pop(0))

    @staticmethod
    def _find_song(name: str):
        song_info = None
        try:
            song_info = YoutubeSearch(name, max_results=1).to_dict()
        except Exception:
            logging.error(f"YoutubeSearch({name}, max_results=1)")
        finally:
            print(song_info[0]['title'])
            if song_info[0]['url_suffix']:
                if is_longer_than_max(song_info[0]['duration']):
                    return None
                return song_info[0]
            else:
                return None

    def _download_then_play(self, name: str):
        while os.path.exists(stubfile):
            try:
                os.remove(stubfile)
            finally:
                pass

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("youtube_dl.YoutubeDL(ydl_opts) as ydl")
            to_download = 'https://www.youtube.com/' + name
            ydl.download([to_download])
            self.current_song = to_download
            self.player.play(FFmpegPCMAudio(stubfile), after=self._on_song_stops)
