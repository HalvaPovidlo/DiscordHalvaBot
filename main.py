import discord
import collector
from discord.ext import commands
from secretConfig import discord_settings

bot = commands.Bot(command_prefix=discord_settings['prefix'])
client = discord.Client()
music_bot = 0


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.message.author.mention}!')


@client.event
async def on_message(message):
    if message.author == client.user:
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
        return "Произошла какая-то ошибка monkaS"
    if counter == 1:
        return "Новая песня добавлена peepoDance"
    return ""


if __name__ == '__main__':
    client.run(discord_settings['token'])
    bot.run(discord_settings['token'])
