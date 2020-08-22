import discord
import collector
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix=settings['prefix'])
client = discord.Client()
music_bot = 0


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.message.author.mention}!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global music_bot
    if message.author == music_bot:
        collector.collect_song(message)
    elif message.content.startswith('<:youtube:335112740957978625> **Searching**'):
        music_bot = message.author
        collector.collect_song(message)

    # await message.channel.send('Hello!')


if __name__ == '__main__':
    client.run(settings['token'])
    bot.run(settings['token'])
