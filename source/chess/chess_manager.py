import berserk
from secretConfig import CHESS_API_TOKEN

session = berserk.TokenSession(CHESS_API_TOKEN)
client = berserk.Client(session=session)


def create_game(variant: str = None):
    return client.challenges.create_open(clock_limit=None,
                                         clock_increment=None,
                                         variant=variant,
                                         position=None)['challenge']['url']
