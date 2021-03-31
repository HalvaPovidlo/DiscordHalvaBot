import logging
import random

from music_stats import google_sheets_api as gs
from music_stats.google_sheets_api import Columns
from utilities import Status
from datetime import date
from time import localtime
import general_messages as gm

MAX_SONGS_FROM_RANDOM = 10
MAX_MESSAGE_LENGTH = 2000


class MusicManager:
    def __init__(self):
        self._songs_list = gs.read_all_data()
        logging.info("Loaded " + str(len(self._songs_list)) + " songs")
        print("Loaded " + str(len(self._songs_list)) + " songs")
        self._songs_map = {}  # [name] -> position in songs_list
        self._any_updates = False
        self._last_update = localtime().tm_min

    def _create_songs_map(self):
        self._songs_map = {}
        for i in range(len(self._songs_list)):
            self._songs_list[i][Columns.COUNTER.value] = int(self._songs_list[i][Columns.COUNTER.value])
            self._songs_map[self._songs_list[i][Columns.NAME.value]] = i

    # Returns the number of times that song was played
    def _add_song_to_sheet(self, name, link="") -> int:
        if not self._songs_map:
            self._create_songs_map()

        today = date.today().strftime("%d/%m/%Y")
        song_index = self._songs_map.get(name, -1)
        if song_index != -1:
            song = self._songs_list[song_index]
            if song[Columns.NAME.value] != name:
                return Status.ERROR.value

            song[Columns.COUNTER.value] += 1
            if song[Columns.LINK.value] == "" and link != "":
                song[Columns.LINK.value] = link

            if len(song) < Columns.LAST_PLAY_DATE.value + 1:
                song.append(today)
            else:
                song[Columns.LAST_PLAY_DATE.value] = today

            return int(song[Columns.COUNTER.value])
        else:
            self._songs_list.append([name, link, 1, today])
            self._songs_map[name] = len(self._songs_list) - 1
            return 1

    def _update_sheet(self):
        if abs(localtime().tm_min - self._last_update) <= 1:
            return

        self._last_update = localtime().tm_min
        logging.info("Updating remote...")
        print("Updating remote...")
        if self._any_updates:
            self._songs_list.sort(key=lambda x: int(x[Columns.COUNTER.value]), reverse=True)
            self._create_songs_map()
            try:
                gs.write_all_data(self._songs_list)
                self._any_updates = False
            except:
                logging.error("gs.write_all_data(songs_list)")
                print("ERROR acquired when gs.write_all_data(songs_list)")
        else:
            logging.info("Nothing to update")
            print("Nothing to update")

    def collect_song(self, message):
        content = message.content
        link = ""
        if content.startswith('**Playing**'):
            # **Playing** 🎶 `Some song name` - Now!
            name = content[content.find('`') + 1:content.rfind('`')]
        elif len(message.embeds) == 1:
            description = message.embeds[0].description

            linkStartIndex = description.find('https://www.youtube.com')
            if linkStartIndex == -1:
                return Status.NO_SONG.value

            # [song name](https://....
            nameEndIndex = linkStartIndex - 2
            if description[nameEndIndex] != ']':
                return Status.NO_SONG.value

            name = description[description.find('[') + 1:nameEndIndex]
            link = description[linkStartIndex:description.rfind(')')]
        else:
            return Status.NO_SONG.value

        print('name: ' + name)
        print('link: ' + link)
        logging.info('name: ' + name)
        logging.info('link: ' + link)

        response = Status.NO_SONG.value
        if name != '':
            response = self._add_song_to_sheet(name, link)
            self._any_updates = True
            self._update_sheet()

        return response

    # Returns message with songs to play
    def random_songs_to_play(self, number=1):
        number %= MAX_SONGS_FROM_RANDOM
        songs_to_play = ""
        for i in range(number):
            songs_to_play += "`!play " + \
                             self._songs_list[random.randint(0, len(self._songs_list))][Columns.NAME.value] + "`\n"
        return songs_to_play

    def radio_song(self):
        index_of_one = 0
        while index_of_one < len(self._songs_list):
            if self._songs_list[index_of_one][Columns.COUNTER.value] == 1:
                break
            index_of_one += 1

        return self._songs_list[random.randrange(index_of_one)][Columns.NAME.value]

    # Return message with songs with substr query
    def find_songs(self, to_find):
        if len(to_find) < 3:
            return gm.SHORT_REQUEST
        to_find = to_find.lower()
        result_songs = ""

        for i in range(len(self._songs_list)):
            if len(result_songs) + len(str(self._songs_list[i][Columns.NAME.value])) + 10 < MAX_MESSAGE_LENGTH:
                if str(self._songs_list[i][Columns.NAME.value]).lower().find(to_find) != -1:
                    result_songs += "`!play " + self._songs_list[i][Columns.NAME.value] + "`\n"

        return result_songs
