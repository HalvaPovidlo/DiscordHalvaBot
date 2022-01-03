import random
from datetime import date
from time import localtime

from discord.ext import commands

import domain.general_messages as gm
from domain import secretConfig
from domain.utilities import log_error_to_channel
from domain.utilities import logerr
from domain.utilities import loginfo
from music.song_info import SongInfo
from music.stats.database import Database
from music.stats.searcher import Searcher
from music.stats.song import Song

prefix = secretConfig.secret_config.discord()["prefix"]

MAX_SONGS_FROM_RANDOM = 10
MAX_MESSAGE_LENGTH = 2000

PREDICTS_NUMBER = 3
PREDICT_LIMIT = 0.08

DATABASE_UPDATE_TIMEOUT = 1  # minutes


class MusicDatabase(commands.Cog):
    def __init__(self, database: Database):
        self.db: Database = database
        self.songs: {str: Song} = self.db.read_data()
        loginfo("Loaded " + str(len(self.songs)) + " songs")
        print("Loaded " + str(len(self.songs)) + " songs")
        self.searcher: Searcher = Searcher(self.songs.keys())
        self._any_updates = False
        self._last_update = localtime().tm_min

        self.songs_list = []
        self._create_song_list()

    # Returns the number of times that song was played
    def _add_song_to_sheet(self, name, link="") -> int:
        today = date.today().strftime("%d/%m/%Y")
        if self.songs.get(name, 0) != 0:
            song: Song = self.songs[name]
            song.counter += 1
            song.date = today
        else:
            song = Song(name, link, 1, today)

        self.songs[name] = song
        return song.counter

    def _create_song_list(self):
        self.songs_list = []
        for key, value in self.songs.items():
            self.songs_list.append([key, value.counter])
        self.songs_list.sort(key=lambda x: int(x[1]), reverse=True)

    def _update_sheet(self):
        if abs(localtime().tm_min - self._last_update) <= DATABASE_UPDATE_TIMEOUT:
            return

        self._last_update = localtime().tm_min
        loginfo("Updating remote...")
        print("Updating remote...")
        if self._any_updates:
            try:
                self.db.write_data(self.songs)
                self._create_song_list()
                self._any_updates = False
            except Exception as e:
                logerr(f"self.db.write_data(self.songs) {e}")
                print(f"self.db.write_data(self.songs) {e}")
        else:
            loginfo("Nothing to update")
            print("Nothing to update")

    def collect_song(self, song_info: SongInfo) -> int:
        response = self._add_song_to_sheet(song_info.title, 'https://www.youtube.com' + song_info.download_link)
        self._any_updates = True
        self._update_sheet()
        return response

    # Returns message with songs to play
    def random_songs_to_play(self, number=1):
        number = min(MAX_SONGS_FROM_RANDOM, number)
        response = ""
        for i in range(number):
            response += "`" + prefix + "play " + self.songs_list[random.randint(0, len(self.songs_list))][0] + "`\n"
        return response

    def get_radio_song(self):
        index_of_one = 0
        while index_of_one < len(self.songs_list):
            if self.songs_list[index_of_one][1] == 1:
                break
            index_of_one += 1
        return self.songs_list[random.randint(0, len(self.songs_list) - 1)][0]

    # Return message with songs with substr query
    def find_songs(self, to_find: str):
        if len(to_find) < 3:
            return gm.SHORT_REQUEST

        prediction = self.searcher.get_prediction(to_find)
        to_find_arr = [to_find]
        counter = 0
        for p in prediction:
            if counter < PREDICTS_NUMBER and p[1] > PREDICT_LIMIT:
                counter += 1
                to_find_arr.append(p[0])

        result_songs = ""
        for i in self.songs.keys():
            song = i.lower()
            for j in range(len(to_find_arr)):
                if song.find(to_find_arr[j]) != -1:
                    if len(result_songs) + len(i) + 10 < MAX_MESSAGE_LENGTH:
                        result_songs += "`" + '$' + "play " + i + "`\n"

        return result_songs

    @commands.command()
    async def random(self, ctx: commands.Context, songs_number: int = 1):
        await ctx.send(self.random_songs_to_play(songs_number))

    @random.error
    async def random_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Аргументом должно быть число DansGame')
            return
        log_error_to_channel(ctx, error)

    @commands.command()
    async def search(self, ctx: commands.Context, to_find: str):
        await ctx.send(self.find_songs(to_find))

    @search.error
    async def search_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Аргументом должна быть строка DansGame')
            return
        log_error_to_channel(ctx, error)
