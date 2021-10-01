import discord.abc
from discord import Message
from discord.ext import commands

import general_messages as gm
from music_stats.music_manager import MusicManager
from secretConfig import discord_settings
from message_handler import MessageHandler, is_from_music_channel, is_from_debug_channel
from chess import chess_manager
import utilities
from movie.movie_manager import MovieManager
from source.music_player.music import Music

bot: discord.ext.commands.Bot = commands.Bot(command_prefix=discord_settings['prefix'])
bot.remove_command('help')

music_manager = MusicManager()
handler = MessageHandler(bot, music_manager)

movie_manager = MovieManager()


async def on_message(message: Message):
    await handler.process_message(message)

bot.add_listener(on_message, 'on_message')


def _log_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    utilities.logerr("{err} in message: {msg}".format(err=error, msg=ctx.message.content))


@bot.event
async def on_command(ctx: commands.Context):
    user = ctx.author
    message: Message = ctx.message
    command = message.content
    utilities.loginfo('{} used :{}: in {}'.format(user, command, message.channel))
    if is_from_music_channel(message) or is_from_debug_channel(message):
        return
    if message.content.startswith("$play") or \
            message.content.startswith("$fs") or \
            message.content.startswith("$skip") or \
            message.content.startswith("$radio") or \
            message.content.startswith("$shuffle") or \
            message.content.startswith("$loop") or \
            message.content.startswith("$pause") or \
            message.content.startswith("$resume"):
        await message.delete()


@bot.check
async def globally_block_on_debug(ctx: commands.Context):
    return discord_settings['debug'] == (str(ctx.message.channel) == 'debug')


@bot.command()
async def hello(ctx: commands.Context):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')


@hello.error
async def hello_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
    _log_error(ctx, error)


@bot.command()
async def help(ctx: commands.Context):
    await ctx.send(gm.HELP)


@help.error
async def guide_error(ctx: commands.Context, error):
    _log_error(ctx, error)


@bot.command()
async def sheet(ctx: commands.Context):
    await ctx.send(gm.SHEET_LINK)


@sheet.error
async def sheet_error(ctx: commands.Context, error):
    _log_error(ctx, error)


@bot.command()
async def github(ctx: commands.Context):
    await ctx.send(gm.GITHUB_LINK)


@github.error
async def github_error(ctx: commands.Context, error):
    _log_error(ctx, error)


@bot.command()
async def random(ctx: commands.Context, songs_number: int = 1):
    await ctx.send(music_manager.random_songs_to_play(songs_number))


@random.error
async def random_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Аргументом должно быть число DansGame')
        return
    _log_error(ctx, error)


@bot.command()
async def search(ctx: commands.Context, to_find: str):
    await ctx.send(music_manager.find_songs(to_find))


@search.error
async def search_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Аргументом должна быть строка DansGame')
        return
    _log_error(ctx, error)


@bot.command()
async def youtube(ctx: commands.Context):
    await ctx.send(gm.YOUTUBE)


@youtube.error
async def youtube_error(ctx: commands.Context, error):
    _log_error(ctx, error)


@bot.command()
async def chess(ctx: commands.Context, variant: str = None):
    await ctx.send(chess_manager.create_game(variant))


@chess.error
async def chess_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Неправильное название режима DansGame. Используй lowerCamelCase')
        return
    _log_error(ctx, error)


@bot.command()
async def film(ctx: commands.Context):
    await ctx.send(gm.FILMS_LINK)


@film.error
async def film_error(ctx: commands.Context, error):
    _log_error(ctx, error)


@bot.command()
async def link(ctx: commands.Context):
    await ctx.send(gm.ALL_LINKS)


@link.error
async def link_error(ctx: commands.Context, error):
    _log_error(ctx, error)


@bot.command()
async def recommend(ctx: commands.Context, name: str):
    await ctx.send(movie_manager.recommend(name))


@recommend.error
async def recommend_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Аргументом должна быть строка DansGame')
        return
    _log_error(ctx, error)


@bot.command()
async def clearchannel(ctx: commands.Context):
    message: Message = ctx.message
    channel: Message = message.channel
    messages = await channel.history(limit=200).flatten()
    for m in messages:
        m: Message = m
        if (m.author.bot or m.content.startswith("!")) and m.author != bot.user:
            await m.delete()


def main():
    utilities.loginfo("started")
    bot.add_cog(Music(bot, music_manager))
    bot.run(discord_settings['token'])


if __name__ == '__main__':
    main()
