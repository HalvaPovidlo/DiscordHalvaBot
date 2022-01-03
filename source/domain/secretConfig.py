import configparser
import sys
from os import path


class SecretConfig:
    def __init__(self, file_path):
        self._config = configparser.ConfigParser()
        if path.exists(file_path):
            self._config.read(file_path)
        else:
            raise FileNotFoundError(f"{file_path} not found")

        self._discord_settings = None
        self._gsheets_settings = None
        self._vk_settings = None
        self._lichess_settings = None

    def discord(self):
        if self._discord_settings is not None:
            return self._discord_settings
        self._discord_settings = read_options(self._config, 'discord', 'token', 'bot', 'prefix')
        if self._discord_settings is None:
            return None

        self._discord_settings['id'] = self._config.getint('discord', 'id')
        self._discord_settings['debug'] = False
        if self._config.has_option('discord', 'debug'):
            self._discord_settings['debug'] = self._config.getboolean('discord', 'debug')

        return self._discord_settings

    def gsheets(self):
        if self._gsheets_settings is not None:
            return self._gsheets_settings

        self._gsheets_settings = {'song': None, 'film': None}
        if self._config.has_option('gsheets', 'song'):
            self._gsheets_settings['song'] = self._config.get('gsheets', 'song')
        if self._config.has_option('gsheets', 'film'):
            self._gsheets_settings['film'] = self._config.get('gsheets', 'film')

        return self._gsheets_settings

    def vk(self):
        if self._vk_settings is not None:
            return self._vk_settings
        self._vk_settings = read_options(self._config, 'vk', 'login', 'password')
        return self._vk_settings

    def lichess(self):
        if self._lichess_settings is not None:
            return self._lichess_settings
        self._lichess_settings = read_options(self._config, 'lichess', 'token')
        return self._lichess_settings


def read_options(config: configparser.ConfigParser, section, *options):
    if not config.has_section(section):
        return None
    settings = {}
    for o in options:
        settings[o] = config.get(section, o)
    return settings


# secret_config = SecretConfig(
#     path.join(path.dirname(path.abspath(sys.modules['__main__'].__file__)), 'secret_config.ini'))
secret_config = SecretConfig('secret_config.ini')
