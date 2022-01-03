import argparse
from os import path

import domain.utilities
from bot import HalvaBot
from chess.chess_manager import ChessManager
from movie.movie_manager import MovieManager
from music.stats.google_sheets_api import GoogleSheets
from music.stats.local_json_db import JSONDatabase
from music.stats.music_database import MusicDatabase

GSHEET_OPTION = "gsheets"
JSON_OPTION = "json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', default=JSON_OPTION
                        , help=f"select which database to use: (default: {JSON_OPTION}) {GSHEET_OPTION}"
                        , choices=[JSON_OPTION, GSHEET_OPTION])
    args = parser.parse_args()
    domain.utilities.loginfo(f"Starting with arguments:\n {args}")

    db = JSONDatabase("music_stats.json")
    if args.database == GSHEET_OPTION:
        db = GoogleSheets()

    bot = HalvaBot(MusicDatabase(db), ChessManager(), MovieManager())
    bot.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
