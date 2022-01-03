import argparse

from bot import HalvaBot
from chess.chess_manager import ChessManager
from movie.movie_manager import MovieManager
from music.stats.google_sheets_api import GoogleSheets
from music.stats.music_database import MusicDatabase


def main():
    bot = HalvaBot(MusicDatabase(GoogleSheets()), ChessManager(), MovieManager())
    bot.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # "address" as positional argument
    parser.add_argument("--test", default="True")
    args = parser.parse_args()
    print(args)
    try:
        main()
    except Exception:
        print("Errrir")
