import discord
from music_manager import manager
import general_messages as MESSAGES
from dirty_talk_detector.dirty_talk_detector import detect
from secretConfig import discord_settings
from secretConfig import gsheets_settings
import utilities as utl

client = discord.Client()
music_bot = 0
DEBUG_MODE = False


def check_dirty(message):
    if message.content != "":
        value = detect(message.content)
        if value > 0.9:
            return MESSAGES.DIRTY_DETECTED + " " + message.author.mention
    return ""


async def add_reactions(message, emoji_list):
    for e in emoji_list:
        await message.add_reaction(e)


async def process_song(message):
    counter = -1
    global music_bot
    if message.author == music_bot:
        counter = manager.collect_song(message)
    elif message.content.startswith('<:youtube:335112740957978625> **Searching**'):
        music_bot = message.author

    if counter == utl.Status.NO_SONG.value:
        return False
    if counter == utl.Status.ERROR.value:
        await message.channel.send(MESSAGES.SONG_ERROR)
    else:
        if counter == 1:
            await message.channel.send(MESSAGES.NEW_SONG)
        await add_reactions(message, utl.number_as_emojis(counter))
    return True


async def process_command(message):
    text = message.content
    prefix = discord_settings['prefix']
    if text.startswith(prefix + "help"):
        await message.channel.send(MESSAGES.HELP)
        return

    if text.startswith(prefix + "sheet") or text.startswith(prefix + "table"):
        await message.channel.send(
            "https://docs.google.com/spreadsheets/d/" + gsheets_settings['id'] + "/edit#gid=0")
        return

    if text.startswith(prefix + "random"):
        await message.channel.send(manager.random_songs_to_play())
        return


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if DEBUG_MODE and str(message.channel) != 'debug':
        return
    if not DEBUG_MODE and str(message.channel) == 'debug':
        return

    print(message.content)
    response = check_dirty(message)
    if response != "":
        await message.channel.send(response)

    if message.content.startswith(discord_settings['prefix']):
        await process_command(message)
        return

    if await process_song(message):
        return


if __name__ == '__main__':
    client.run(discord_settings['token'])
