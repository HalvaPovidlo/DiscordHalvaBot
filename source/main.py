import argparse
import configparser
from os import path

import domain.utilities
from bot import HalvaBot
from chess.chess_manager import ChessManager
from domain.secretConfig import secret_config
from movie.movie_manager import MovieManager
from music.stats.google_sheets_api import GoogleSheets
from music.stats.local_json_db import JSONDatabase
from music.stats.music_database import MusicDatabase

GSHEET_OPTION = "gsheets"
JSON_OPTION = "json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', default=JSON_OPTION
                        , help=f"select which database to use (default: {JSON_OPTION})"
                        , choices=[JSON_OPTION, GSHEET_OPTION])
    args = parser.parse_args()
    domain.utilities.loginfo(f"Starting with arguments:\n {args}")

    db = JSONDatabase("music_stats.json")
    if args.database == GSHEET_OPTION:
        if secret_config.gsheets() is None:
            raise configparser.NoSectionError('gsheets')
        if secret_config.gsheets()['song'] is None:
            raise configparser.NoOptionError('song', 'gsheets')
        db = GoogleSheets()

    cogs = []
    if secret_config.gsheets() is not None and secret_config.gsheets()['film'] is not None:
        cogs.append(MovieManager())
    if secret_config.lichess() is not None:
        cogs.append(ChessManager())

    bot = HalvaBot(MusicDatabase(db), cogs)
    bot.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
