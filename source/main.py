import logging
from discord.ext import commands

import general_messages as gm
from music_stats.music_manager import MusicManager
from secretConfig import discord_settings
from message_handler import MessageHandler
from chess import chess_manager

bot = commands.Bot(command_prefix=discord_settings['prefix'])

music_manager = MusicManager()
handler = MessageHandler(bot, music_manager)
bot.remove_command('help')


async def on_message(message):
    await handler.process_message(message)

bot.add_listener(on_message, 'on_message')


def _log_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    logging.error("{err} in message: {msg}".format(err=error, msg=ctx.message.content))


@bot.check
async def globally_block_on_debug(ctx):
    return discord_settings['debug'] == (str(ctx.message.channel) == 'debug')


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
async def help(ctx):
    await ctx.send(gm.HELP)


@help.error
async def guide_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def sheet(ctx):
    await ctx.send(gm.SHEET_LINK)


@sheet.error
async def sheet_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def github(ctx):
    await ctx.send(gm.GITHUB_LINK)


@github.error
async def github_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def random(ctx, songs_number: int = 1):
    await ctx.send(music_manager.random_songs_to_play(songs_number))


@random.error
async def random_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Аргументом должно быть число DansGame')
        return
    _log_error(ctx, error)


@bot.command()
async def search(ctx, to_find: str):
    await ctx.send(music_manager.find_songs(to_find))


@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Аргументом должна быть строка DansGame')
        return
    _log_error(ctx, error)


@bot.command()
async def youtube(ctx):
    await ctx.send(gm.YOUTUBE)


@youtube.error
async def youtube_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def chess(ctx, variant: str = None):
    await ctx.send(chess_manager.create_game(variant))


@chess.error
async def chess_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Неправильное название режима DansGame. Используй lowerCamelCase')
        return
    _log_error(ctx, error)


@bot.command()
async def link(ctx):
    await ctx.send(gm.ALL_LINKS)


@link.error
async def link_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def film(ctx):
    await ctx.send(gm.FILMS_LINK)


@film.error
async def film_error(ctx, error):
    _log_error(ctx, error)


def main():
    bot.run(discord_settings['token'])


if __name__ == '__main__':
    main()
