import os

import discord
import vk_api
from vk_api.audio import VkAudio
from ffmpy3 import FFmpeg

from domain.utilities import find_free_name, loginfo, logerr
from music.player.Searcher.searcher import Searcher
from music.song_info import SongInfo

from secretConfig import vk

stubfile = "stubname.mp3"

ffmpeg_options = {
    'options': '-vn'
}


class VK(Searcher):
    def __init__(self, *, source, song_info, filename, volume=0.5):
        if source:
            super().__init__(source, song_info=song_info, filename=filename, volume=volume)
        else:
            super().__init__(discord.FFmpegPCMAudio(stubfile, **ffmpeg_options),
                             song_info=song_info, volume=volume, filename=filename)
            self.vk_session = vk_api.VkApi(vk['login'], vk['password'])
            try:
                self.vk_session.auth()
            except vk_api.AuthError as error_msg:
                print(error_msg)
                logerr(str(error_msg))
                return
            self.vk_audio = vk_api.audio.VkAudio(self.vk_session)

    @classmethod
    async def download(cls, song_info: SongInfo, *, loop=None, stream=False) -> Searcher:
        """Overrides Searcher.download"""
        song_filename = find_free_name(song_info.title + ".mp3")
        filename = load(song_info.download_link, song_filename)
        os.rename(filename, song_filename)

        return cls(source=discord.FFmpegPCMAudio(song_filename, **ffmpeg_options), song_info=song_info
                   , filename=song_filename)

    def find(self, query: str) -> SongInfo:
        print("Finding", query)
        try:
            song_info: SongInfo = SongInfo()
            search_result = list(self.vk_audio.search(query, count=1))
            if len(search_result) == 0:
                loginfo(f"vk_audio({query}, count=1) can't find any song")
                return None
            out = search_result[0]
            song_info.fromVK(out)
            print("Found", song_info.title)
            loginfo(f"Found {song_info.title} : {song_info.duration}")
            return song_info
        except Exception as e:
            logerr(f"vk_audio({query}, count=1) {e}")
            self.vk_session.auth()
            self.vk_audio = vk_api.audio.VkAudio(self.vk_session)
            return None


def load(inputs_path, outputs_path):
    """
    :param inputs_path: input file input dictionary format {file: operation}
    :param outputs_path: The output file is transferred to the dictionary format {file: operation}
    :return:
    """
    f = FFmpeg(
        global_options=["-hide_banner", "-loglevel error"],
        inputs={inputs_path: None},
        outputs={outputs_path: '-c copy',
                 }
    )
    print(f.cmd)
    f.run()
    return outputs_path
