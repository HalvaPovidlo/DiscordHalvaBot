import discord
from music_collector import collector
import general_messages as MESSAGES
from dirty_talk_detector.dirty_talk_detector import detect
from discord.ext import commands
from secretConfig import discord_settings

bot = commands.Bot(command_prefix=discord_settings['prefix'])
client = discord.Client()
music_bot = 0


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.message.author.mention}!')


def check_pedo(message):
    if message.content != "":
        value = detect(message.content)
        if value > 0.9:
            return MESSAGES.PEDO_DETECTED + " " + message.author.mention
    return ""


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = check_pedo(message)
    if response != "":
        await message.channel.send(response)

    if message.content.startswith("$help"):
        await message.channel.send(MESSAGES.HELP)
        return

    if message.content.startswith("$sheet") or message.content.startswith("$table"):
        await message.channel.send(
            "https://docs.google.com/spreadsheets/d/163dwWivbX6tPkMgKZrLiNuxiIFaS0M5oENUuxTI2JSg/edit#gid=0")
        return

    response = process_song(message)
    if response != "":
        await message.channel.send(response)
        return


def process_song(message):
    counter = -1
    global music_bot
    if message.author == music_bot:
        counter = collector.collect_song(message)
    elif message.content.startswith('<:youtube:335112740957978625> **Searching**'):
        music_bot = message.author
        counter = collector.collect_song(message)

    if counter == 0:
        return MESSAGES.SONG_ERROR
    if counter == 1:
        return MESSAGES.NEW_SONG
    return ""


if __name__ == '__main__':
    client.run(discord_settings['token'])
    bot.run(discord_settings['token'])
