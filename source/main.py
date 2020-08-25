import discord
from music_collector import collector
import general_messages as MESSAGES
from dirty_talk_detector.dirty_talk_detector import detect
from discord.ext import commands
from secretConfig import discord_settings
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
        counter = collector.collect_song(message)
    elif message.content.startswith('<:youtube:335112740957978625> **Searching**'):
        music_bot = message.author
        counter = collector.collect_song(message)

    if counter == -1:
        return False
    if counter == 0:
        await message.channel.send(MESSAGES.SONG_ERROR)
    else:
        if counter == 1:
            await message.channel.send(MESSAGES.NEW_SONG)
        await add_reactions(message, utl.number_as_emojis(counter))
    return True


async def process_command(message):
    if message.content.startswith("$help"):
        await message.channel.send(MESSAGES.HELP)
        return

    if message.content.startswith("$sheet") or message.content.startswith("$table"):
        await message.channel.send(
            "https://docs.google.com/spreadsheets/d/163dwWivbX6tPkMgKZrLiNuxiIFaS0M5oENUuxTI2JSg/edit#gid=0")
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

    if message.content.startswith("$"):
        await process_command(message)
        return

    if await process_song(message):
        return


if __name__ == '__main__':
    client.run(discord_settings['token'])
