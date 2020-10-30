from discord.ext import commands

from music_manager import manager
import general_messages as gm
from secretConfig import discord_settings


bot = commands.Bot(command_prefix=discord_settings['prefix'])
DEBUG_MODE = discord_settings['debug']


def _log_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    print("ERROR: ", error)
    print("In message: ", ctx.message.content)


@bot.check
async def globally_block_on_debug(ctx):
    return DEBUG_MODE == (str(ctx.message.channel) == 'debug')


@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')


@hello.error
async def hello_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
    _log_error(ctx, error)


@bot.command()
async def guide(ctx):
    await ctx.send(gm.HELP)


@guide.error
async def guide_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def sheet(ctx):
    await ctx.send(gm.SHEET_LINK)


@sheet.error
async def sheet_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def random(ctx, songs_number: int = 1):
    manager.rerun_timers()
    await ctx.send(manager.random_songs_to_play(songs_number))


@random.error
async def random_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Вторым аргументом должно быть число DansGame')
        return
    _log_error(ctx, error)


if __name__ == '__main__':
    bot.run(discord_settings['token'])
