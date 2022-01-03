import berserk
from discord.ext import commands
from domain.secretConfig import CHESS_API_TOKEN

from domain.utilities import log_error_to_channel

session = berserk.TokenSession(CHESS_API_TOKEN)
client = berserk.Client(session=session)


class ChessManager(commands.Cog):
    def create_game(self, variant: str = None):
        return client.challenges.create_open(clock_limit=None,
                                             clock_increment=None,
                                             variant=variant,
                                             position=None)['challenge']['url']

    @commands.command()
    async def chess(self, ctx: commands.Context, variant: str = None):
        await ctx.send(self.create_game(variant))

    @chess.error
    async def chess_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Неправильное название режима DansGame. Используй lowerCamelCase')
            return
        log_error_to_channel(ctx, error)