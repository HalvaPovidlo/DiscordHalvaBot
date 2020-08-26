from threading import Timer
from threading import Lock

from music_collector import google_sheets_api as gs
from music_collector.google_sheets_api import Columns

songs_map = {}
songs_list = gs.read_all_data()
any_updates = False
any_updates_lock = Lock()
update_timer = None


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
        songs_list[song_index][Columns.COUNTER.value] += 1
        if songs_list[song_index][Columns.LINK.value] == "" and link != "":
            songs_list[song_index][Columns.LINK.value] = link

        return int(songs_list[song_index][Columns.COUNTER.value])
    else:
        songs_list.append([name, link, 1])
        songs_map[name] = len(songs_list) - 1
        return 1


def update_sheet():
    print("Updating...")
    any_updates_lock.acquire()
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
    any_updates_lock.release()


def rerun_timer():
    global update_timer
    if update_timer:
        update_timer.cancel()

    update_timer = Timer(10.0, update_sheet)
    update_timer.start()


def collect_song(message):
    rerun_timer()
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
            return -1

        # [song name](https://....
        nameEndIndex = linkStartIndex - 2
        if description[nameEndIndex] != ']':
            return -1

        name = description[description.find('[') + 1:nameEndIndex]
        link = description[linkStartIndex:description.rfind(')')]
    else:
        return -1

    print('name: ' + name)
    print('link: ' + link)

    response = -1
    if name != '':
        response = add_song_to_sheet(name, link)
        any_updates_lock.acquire()
        global any_updates
        any_updates = True
        any_updates_lock.release()

    return response


if __name__ == '__main__':
    print("Hello World!!!")
