import logging
import random


class MusicPlayer:
    def __init__(self):
        self._playlist = []

    def queue_song(self, song: str):
        self._playlist.append(song)

    def shuffle(self):
        random.shuffle(self._playlist)

#    def
