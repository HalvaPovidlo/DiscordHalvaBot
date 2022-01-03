import discord.abc
from discord import Message
from discord.ext import commands

import domain.general_messages as gm
import domain.utilities
from secretConfig import discord_settings
from message_handler import MessageHandler, is_from_music_channel, is_from_debug_channel


bot: discord.ext.commands.Bot = commands.Bot(command_prefix=discord_settings['prefix'])
bot.remove_command('help')

handler = MessageHandler(bot)


class HalvaBot:
    def __init__(self, *cogs: commands.Cog):
        for cog in cogs:
            bot.add_cog(cog)
        domain.utilities.loginfo("HalvaBot started!")


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
    if message.content.startswith(discord_settings['prefix']):
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
        if m.author.bot or m.content.startswith("!"):
            await m.delete()


def main():
    domain.utilities.loginfo("started")


    bot.run(discord_settings['token'])
