import configparser
import sys
from os import path


class SecretConfig:
    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        if path.exists(file_path):
            self.config.read(file_path)
        else:
            raise FileNotFoundError(f"{file_path} not found")

        self.discord_settings = None
        self.gsheets_settings = None
        self.vk_settings = None
        self.lichess_settings = None

    def discord(self):
        if self.discord_settings is not None:
            return self.discord_settings
        self.discord_settings = read_options(self.config, 'discord', 'token', 'bot', 'prefix')
        if self.discord_settings is None:
            return None

        self.discord_settings['id'] = self.config.getint('discord', 'id')
        self.discord_settings['debug'] = False
        if self.config.has_option('discord', 'debug'):
            self.discord_settings['debug'] = self.config.getboolean('discord', 'debug')

        return self.discord_settings

    def gsheets(self):
        if self.gsheets_settings is not None:
            return self.gsheets_settings
        self.gsheets_settings = read_options(self.config, 'gsheets', 'id', 'film')
        return self.gsheets_settings

    def vk(self):
        if self.vk_settings is not None:
            return self.vk_settings
        self.vk_settings = read_options(self.config, 'vk', 'login', 'password')
        return self.vk_settings

    def lichess(self):
        if self.lichess_settings is not None:
            return self.lichess_settings
        self.lichess_settings = read_options(self.config, 'lichess', 'token')
        return self.lichess_settings


def read_options(config: configparser.ConfigParser, section, *options):
    if not config.has_section(section):
        return None
    settings = {}
    for o in options:
        settings[o] = config.get(section, o)
    return settings


secret_config = SecretConfig(
    path.join(path.dirname(path.abspath(sys.modules['__main__'].__file__)), 'secret_config.ini'))
