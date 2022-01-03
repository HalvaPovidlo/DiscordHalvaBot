import berserk
from discord.ext import commands
from domain.secretConfig import secret_config

from domain.utilities import log_error_to_channel


class ChessManager(commands.Cog):
    def __init__(self):
        self.session = berserk.TokenSession(secret_config.lichess()['token'])
        self.client = berserk.Client(session=self.session)

    def create_game(self, variant: str = None):
        return self.client.challenges.create_open(clock_limit=None,
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