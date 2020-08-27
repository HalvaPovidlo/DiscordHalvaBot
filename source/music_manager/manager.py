from threading import Timer
from threading import Lock
import random

from music_manager import google_sheets_api as gs
from music_manager.google_sheets_api import Columns
from utilities import Status

songs_map = {}
songs_list = gs.read_all_data()
any_updates = False
read_write_sheet_lock = Lock()
write_timer = None
load_timer = None

MAX_SONGS_FROM_RANDOM = 10


def create_songs_map():
    global songs_map
    songs_map = {}
    for i in range(len(songs_list)):
        songs_list[i][Columns.COUNTER.value] = int(songs_list[i][Columns.COUNTER.value])
        songs_map[songs_list[i][Columns.NAME.value]] = i


# Returns the number of times that song was played
def add_song_to_sheet(name, link=""):
    global songs_list
    global songs_map

    if not songs_map:
        create_songs_map()

    song_index = songs_map.get(name, -1)
    if song_index != -1:
        song = songs_list[song_index]
        if song[Columns.NAME.value] != name:
            return Status.ERROR.value

        song[Columns.COUNTER.value] += 1
        if song[Columns.LINK.value] == "" and link != "":
            song[Columns.LINK.value] = link

        return int(songs_list[song_index][Columns.COUNTER.value])
    else:
        songs_list.append([name, link, 1])
        songs_map[name] = len(songs_list) - 1
        return 1


def update_sheet():
    read_write_sheet_lock.acquire()
    print("Updating remote...")
    try:
        global any_updates
        if any_updates:
            songs_list.sort(key=lambda x: int(x[Columns.COUNTER.value]), reverse=True)
            create_songs_map()
            try:
                gs.write_all_data(songs_list)
                any_updates = False
            except:
                print("ERROR acquired when gs.write_all_data(songs_list)")
        else:
            print("Nothing to update")
    except:
        print("ERROR in update_sheet")
    read_write_sheet_lock.release()


def update_local_data():
    read_write_sheet_lock.acquire()
    print("Updating local...")
    global songs_list
    try:
        new_songs_list = gs.read_all_data()
        print("Local vs remote difference: ", len(songs_list) - len(new_songs_list))
        songs_list = new_songs_list
        create_songs_map()
    except:
        print("ERROR acquired when gs.read_all_data()")
    read_write_sheet_lock.release()


def rerun_timers():
    global write_timer
    global load_timer

    if write_timer:
        write_timer.cancel()
    write_timer = Timer(10.0, update_sheet)
    write_timer.start()

    if load_timer:
        load_timer.cancel()
    load_timer = Timer(60.0, update_local_data)
    load_timer.start()


def collect_song(message):
    rerun_timers()
    content = message.content
    print(content)
    name = ""
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

    response = Status.NO_SONG.value
    if name != '':
        read_write_sheet_lock.acquire()
        response = add_song_to_sheet(name, link)
        global any_updates
        any_updates = True
        read_write_sheet_lock.release()

    return response


# Returns message with songs to play
def random_songs_to_play(number=1):
    number %= MAX_SONGS_FROM_RANDOM
    songs_to_play = ""
    read_write_sheet_lock.acquire()
    for i in range(number):
        songs_to_play += "`!play " + songs_list[random.randint(0, len(songs_list))][Columns.NAME.value] + "`\n"
    read_write_sheet_lock.release()
    return songs_to_play
