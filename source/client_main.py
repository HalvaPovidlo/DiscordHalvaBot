import discord

from music_manager import manager
import general_messages as gm
from dirty_talk_detector.dirty_talk_detector import detect
from secretConfig import discord_settings
import utilities as utl
from random import randint

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


def is_from_music_channel(msg) -> bool:
    return str(msg.channel) == 'music'


def is_from_debug_channel(msg) -> bool:
    return str(msg.channel) == 'debug'


async def delete_music_message(message):
    if is_from_music_channel(message) or is_from_debug_channel(message):
        return
    if message.author == music_bot or message.content.startswith("!play") or message.content.startswith("!fs"):
        await message.delete()


async def process_song(message):
    counter = -1
    global music_bot

    if message.author == music_bot or message.content.startswith('<:youtube:335112740957978625> **Searching**'):
        music_bot = message.author
        counter = manager.collect_song(message)

    if counter == utl.Status.NO_SONG.value:
        return False
    if counter == utl.Status.ERROR.value:
        await message.channel.send(gm.SONG_ERROR)
    else:
        if counter == 1 and (is_from_music_channel(message) or is_from_debug_channel(message)):
            await message.channel.send(gm.NEW_SONG[randint(0, len(gm.NEW_SONG) - 1)])
        await add_reactions(message, utl.number_as_emojis(counter))
    return True


def skip_message(message) -> bool:
    return message.author == client.user or\
           DEBUG_MODE != is_from_debug_channel(message) or\
           message.content.startswith(discord_settings['prefix'])


@client.event
async def on_message(message):
    if skip_message(message):
        return

    message_lower = message.content.lower()
    if message_lower.find("рус") != -1 or message_lower.find("рос") != -1:
        await message.channel.send(message.author.mention + " РУССКИЕ ВПЕРЕД!!!")

    response = check_dirty(message)
    if response != "":
        await message.channel.send(response)

    await process_song(message)

    await delete_music_message(message)


if __name__ == '__main__':
    client.run(discord_settings['token'])
