import asyncio

import discord

from discord import VoiceClient
import queue
from discord.ext import commands

from message_handler import is_from_music_channel, is_from_debug_channel
import music.player.player_messages as pm
from music.player.Searcher.YoutubeDL import YTDLSource
from music.player.Searcher.searcher import Searcher
from music.song_info import SongInfo
from music.stats.music_database import MusicDatabase
from utilities import logerr, number_to_emojis


class SongQuery:
    def __init__(self, url, searcher: Searcher):
        self.url = url
        self.searcher = searcher


class Music(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot, manager: MusicDatabase):
        self.bot: discord.ext.commands.Bot = bot
        self.voiceClient: VoiceClient = None
        self.is_loop: bool = False
        self.is_radio: bool = False
        self.current_song: Searcher = None
        self.manager: MusicDatabase = manager
        self.ytdl: Searcher = YTDLSource(source=None, data={}, filename="")
        self.playlist = queue.Queue()  # of SongQueries
        self.is_playing = False  # Atomic

    @commands.command()
    async def play(self, ctx, *, query):
        """Playing song from youtube"""
        await ctx.send(pm.SEARCHING)
        async with ctx.typing():
            song_info: SongInfo = self.ytdl.find(query)
            if song_info:
                await self.collect_data(song_info, ctx)
                self.playlist.put(SongQuery(song_info.url_suffix, self.ytdl))
                await self.run_playlist()
            else:
                await ctx.send(pm.NO_MATCH)

    async def load_with(self, searcher: Searcher, url) -> Searcher:
        try:
            return await searcher.from_url(url, loop=self.bot.loop)
        except Exception:
            logerr("Find song impossible")
        return None

    def is_channel_empty(self) -> bool:
        return len(self.voiceClient.channel.voice_states.keys()) == 1

    async def run_playlist(self):
        if self.is_channel_empty():
            await self.disconnect()
            return

        if self.is_playing:
            return
        self.is_playing = True

        if self.current_song:
            if self.is_loop:
                self.voiceClient.play(self.current_song, after=self._after_start_playlist)
                return

        if self.playlist.empty():
            if self.is_radio:
                url = self.ytdl.find(self.manager.get_radio_song()).url_suffix
                song = await self.load_with(self.ytdl, url)
            else:
                await self.disconnect()
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

    async def collect_data(self, song_info: SongInfo, ctx):
        counter = self.manager.collect_song(song_info)
        emojis = number_to_emojis(counter)
        if self.is_playing:
            await send_to_music(ctx, f"{pm.ENQUEUE.format(song_name=song_info.title)}  {emojis}")
        else:
            await send_to_music(ctx, f"{pm.START_PLAYING.format(song_name=song_info.title)}  {emojis}")

    @commands.command()
    async def radio(self, ctx):
        self.is_radio = not self.is_radio
        if self.is_radio:
            await self.run_playlist()
            await send_to_music(ctx, pm.RADIO_ENABLED)
        else:
            await send_to_music(ctx, pm.RADIO_DISABLED)

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
    async def loop(self, ctx):
        self.is_loop = not self.is_loop
        if self.is_loop:
            await send_to_music(ctx, pm.LOOP_ENABLED)
        else:
            await send_to_music(ctx, pm.LOOP_DISABLED)

    @commands.command()
    async def skip(self, ctx):
        self.voiceClient.stop()
        await send_to_music(ctx, pm.SKIPPED)

    @commands.command()
    async def current(self, ctx):
        if self.current_song:
            await send_to_music(ctx, pm.CURRENT + " " + self.current_song.title)
        else:
            await send_to_music(ctx, pm.NO_CURRENT)

    @commands.command()
    async def disconnect(self, ctx=None):
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
        if self.voiceClient is None or not self.voiceClient.is_connected():
            if ctx.author.voice:
                self.voiceClient = await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        else:
            await ctx.send("You are not connected to the my voice channel.")

    @loop.before_invoke
    @skip.before_invoke
    async def is_bot_available(self, ctx):
        if self.voiceClient is None or not self.voiceClient.is_playing():
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Bot not connected or not playing anything.")


async def send_to_music(ctx, msg: str):
    if is_from_music_channel(ctx.message) or is_from_debug_channel(ctx.message):
        await ctx.send(msg)
