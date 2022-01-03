import discord.abc
from discord import Message
from discord.ext import commands

import domain.general_messages as gm
import domain.utilities
from music.player.cog import MusicCog
from music.stats.music_database import MusicDatabase
from domain.secretConfig import secret_config as sc
from message_handler import MessageHandler, is_from_music_channel, is_from_debug_channel

# Strange temporary solution of using global bot instance TODO
bot: discord.ext.commands.Bot = commands.Bot(command_prefix=sc.discord()['prefix'])
bot.remove_command('help')

handler = MessageHandler(bot)


async def on_message(message: Message):
    await handler.process_message(message)

bot.add_listener(on_message, 'on_message')


@bot.event
async def on_command(ctx: commands.Context):
    user = ctx.author
    message: Message = ctx.message
    command = message.content
    domain.utilities.loginfo('{} used :{}: in {}'.format(user, command, message.channel))
    if is_from_music_channel(message) or is_from_debug_channel(message):
        return
    if message.content.startswith(sc.discord()['prefix']):
        await message.delete()


@bot.check
async def globally_block_on_debug(ctx: commands.Context):
    return sc.discord()['debug'] == (str(ctx.message.channel) == 'debug')


@bot.command()
async def hello(ctx: commands.Context):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')


@hello.error
async def hello_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
    domain.utilities.log_error_to_channel(ctx, error)


@bot.command()
async def help(ctx: commands.Context):
    await ctx.send(gm.HELP)


@bot.command()
async def sheet(ctx: commands.Context):
    await ctx.send(gm.SHEET_LINK)


@bot.command()
async def link(ctx: commands.Context):
    await ctx.send(gm.ALL_LINKS)


@bot.command()
async def clearchannel(ctx: commands.Context):
    message: Message = ctx.message
    channel: Message = message.channel
    messages = await channel.history(limit=200).flatten()
    for m in messages:
        m: Message = m
        if m.author.bot or m.content.startswith("!") or m.content.startswith(sc.discord()['prefix']):
            await m.delete()


class HalvaBot:
    def __init__(self, md: MusicDatabase,  *cogs: commands.Cog):
        self.bot = bot
        self.bot.add_cog(md)
        # Bad TODO
        self.bot.add_cog(MusicCog(self.bot, md))

        for cog in cogs:
            self.bot.add_cog(cog)
        domain.utilities.loginfo("HalvaBot created!")

    def run(self):
        domain.utilities.loginfo("HalvaBot running!")
        self.bot.run(sc.discord()['token'])
