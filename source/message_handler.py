from random import randint

from discord import Client

from music_stats.music_manager import MusicManager
import general_messages as gm
from dirty_talk_detector.dirty_talk_detector import detect
from secretConfig import discord_settings
import utilities as utl


def is_from_debug_channel(msg) -> bool:
    return str(msg.channel) == 'debug'


def is_from_music_channel(msg) -> bool:
    return str(msg.channel) == 'music'


class MessageHandler:
    """The class handles messages that were not started with the bot prefix."""

    def __init__(self, client: Client, manager: MusicManager):
        self._client = client
        self._is_debug_mode = discord_settings['debug']
        self._music_bot = None
        self._manager = manager

    async def delete_music_message(self, message):
        if is_from_music_channel(message) or is_from_debug_channel(message):
            return
        if message.author == self._music_bot or \
                message.content.startswith("!play") or \
                message.content.startswith("!fs"):
            await message.delete()

    async def process_song(self, message):
        counter = utl.Status.NO_SONG.value

        if message.author == self._music_bot or message.content.startswith('<:youtube:335112740957978625> **Searching'):
            self._music_bot = message.author
            counter = self._manager.collect_song(message)

        if counter == utl.Status.NO_SONG.value:
            return

        if counter == utl.Status.ERROR.value:
            await message.channel.send(gm.ANY_ERROR)
        else:
            if counter == 1 and (is_from_music_channel(message) or is_from_debug_channel(message)):
                await message.channel.send(gm.NEW_SONG[randint(0, len(gm.NEW_SONG) - 1)])
            await self.add_reactions(message, utl.number_as_emojis(counter))

    def skip_message(self, message) -> bool:
        return message.author == self._client.user or \
               self._is_debug_mode != is_from_debug_channel(message) or \
               message.content.startswith(discord_settings['prefix'])

    async def process_message(self, message):
        if self.skip_message(message):
            return

        message_lower = message.content.lower()
        if message_lower.find("рус") != -1 or message_lower.find("рос") != -1:
            await message.channel.send(message.author.mention + " РУССКИЕ ВПЕРЕД!!!")

        response = self.check_dirty(message)
        if response != "":
            await message.channel.send(response)

        await self.process_song(message)

        await self.delete_music_message(message)

    @staticmethod
    def check_dirty(message) -> str:
        """
        Checks message on dirty talk.
        :param message:
        :return: Response for the dirty talker or an empty string
        """
        if message.content != "":
            value = detect(message.content)
            if value > 0.9:
                return gm.DIRTY_DETECTED + " " + message.author.mention
        return ""

    @staticmethod
    async def add_reactions(message, emoji_list):
        for e in emoji_list:
            await message.add_reaction(e)
