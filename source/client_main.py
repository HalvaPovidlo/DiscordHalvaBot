import discord

from music_manager import manager
import general_messages as gm
from dirty_talk_detector.dirty_talk_detector import detect
from secretConfig import discord_settings
import utilities as utl

client = discord.Client()
music_bot = 0
DEBUG_MODE = discord_settings['debug']


def check_dirty(message):
    if message.content != "":
        value = detect(message.content)
        if value > 0.9:
            return gm.DIRTY_DETECTED + " " + message.author.mention
    return ""


async def add_reactions(message, emoji_list):
    for e in emoji_list:
        await message.add_reaction(e)


async def process_song(message):
    counter = -1
    global music_bot
    if message.author == music_bot and not DEBUG_MODE:
        counter = manager.collect_song(message)
    elif message.content.startswith('<:youtube:335112740957978625> **Searching**'):
        music_bot = message.author

    if counter == utl.Status.NO_SONG.value:
        return False
    if counter == utl.Status.ERROR.value:
        await message.channel.send(gm.SONG_ERROR)
    else:
        if counter == 1:
            await message.channel.send(gm.NEW_SONG)
        await add_reactions(message, utl.number_as_emojis(counter))
    return True


def skip_message(message):
    return message.author == client.user or DEBUG_MODE != (str(message.channel) == 'debug') or \
           message.content.startswith(discord_settings['prefix'])


@client.event
async def on_message(message):
    if skip_message(message):
        return

    if message.content.lower().find("русс") != -1:
        await message.channel.send(message.author.mention + " РУССКИЕ ВПЕРЕД!!!")

    response = check_dirty(message)
    if response != "":
        await message.channel.send(response)

    if await process_song(message):
        return


if __name__ == '__main__':
    client.run(discord_settings['token'])
