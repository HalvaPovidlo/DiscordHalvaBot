from discord import Client
from discord import Message

import general_messages as gm
from dirty_talk_detector.dirty_talk_detector import detect
from secretConfig import discord_settings


def is_from_debug_channel(msg: Message) -> bool:
    return str(msg.channel) == 'debug'


def is_from_music_channel(msg: Message) -> bool:
    return str(msg.channel) == 'music'


class MessageHandler:
    """The class handles messages that were not started with the bot prefix."""

    def __init__(self, client: Client):
        self._client: Client = client
        self._is_debug_mode: bool = discord_settings['debug']
        self._music_bot = None

    async def delete_music_message(self, message: Message):
        if is_from_music_channel(message) or is_from_debug_channel(message):
            return
        if message.author == self._music_bot or \
                message.content.startswith("!play") or \
                message.content.startswith("!fs"):
            await message.delete()

    def skip_message(self, message: Message) -> bool:
        return message.author == self._client.user or \
               self._is_debug_mode != is_from_debug_channel(message) or \
               message.content.startswith(discord_settings['prefix'])

    async def process_message(self, message: Message):
        if self.skip_message(message):
            return

        message_lower = message.content.lower()
        if message_lower.find("рус") != -1 or message_lower.find("рос") != -1:
            await message.channel.send(message.author.mention + " РУССКИЕ ВПЕРЕД!!!")

        response = self.check_dirty(message)
        if response != "":
            await message.channel.send(response)

        await self.delete_music_message(message)

    @staticmethod
    def check_dirty(message: Message) -> str:
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
