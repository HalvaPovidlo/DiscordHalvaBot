import asyncio

import discord

from discord import VoiceClient
import queue
from discord.ext import commands

from source.music_player.Searcher.YoutubeDL import YTDLSource
from source.music_player.Searcher.searcher import Searcher
from source.music_stats.music_manager import MusicManager
from source.utilities import logerr


class SongQuery:
    def __init__(self, url, searcher: Searcher):
        self.url = url
        self.searcher = searcher


class Music(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot, manager: MusicManager):
        self.bot: discord.ext.commands.Bot = bot
        self.voiceClient: VoiceClient = None
        self.is_loop: bool = False
        self.is_radio: bool = False
        self.current_song: Searcher = None
        self.manager: MusicManager = manager
        self.ytdl: Searcher = YTDLSource(source=None, data={}, filename="")
        self.playlist = queue.Queue()  # of SongQueries
        self.is_playing = False  # Atomic

    @commands.command()
    async def play(self, ctx, *, query):
        async with ctx.typing():
            song = self.ytdl.find(query)
            if song:
                self.playlist.put(SongQuery(song["url_suffix"], self.ytdl))
                await self.run_playlist()
            else:
                return

        await ctx.send('Now playing: {}'.format(song["title"]))

    async def load_with(self, searcher: Searcher, url) -> Searcher:
        try:
            return await searcher.from_url(url, loop=self.bot.loop)
        except Exception:
            logerr("Find song impossible")
        return None

    async def run_playlist(self):
        if self.is_playing:
            return
        self.is_playing = True

        if self.current_song:
            if self.is_loop:
                self.voiceClient.play(self.current_song, after=self._after_start_playlist)
                return
            else:
                self.current_song.delete()

        if self.playlist.empty():
            if self.is_radio:
                url = self.ytdl.find(self.manager.radio_song())["url_suffix"]
                song = await self.load_with(self.ytdl, url)
            else:
                await self.stop()
                return
        else:
            sq: SongQuery = self.playlist.get()
            song = await self.load_with(sq.searcher, sq.url)

        self.current_song = song
        if song:
            self.voiceClient.play(song, after=self._after_start_playlist)
        else:
            self._after_start_playlist(None)

    def _after_start_playlist(self, err):
        self.is_playing = False
        if err:
            logerr(err)
        else:
            asyncio.ensure_future(self.run_playlist(), loop=self.bot.loop)

    @commands.command()
    async def radio(self, ctx):
        self.is_radio = not self.is_radio
        await self.run_playlist()

    # @commands.command()
    # async def stream(self, ctx, *, url):
    #     """Streams from a url (same as yt, but doesn't predownload)"""
    #
    #     async with ctx.typing():
    #         player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
    #         self.voiceClient.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #     await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def skip(self, ctx):
        self.voiceClient.stop()

    @commands.command()
    async def stop(self, ctx=None):
        """Stops and disconnects the bot from voice"""
        while not self.playlist.empty():
            self.playlist.get()
        self.is_loop = False
        self.current_song = None
        self.is_radio = False
        self.is_playing = False
        await self.voiceClient.disconnect()

    # @stream.before_invoke
    @play.before_invoke
    @radio.before_invoke
    async def ensure_voice(self, ctx):
        if self.voiceClient is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                self.voiceClient = ctx.voice_client
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
