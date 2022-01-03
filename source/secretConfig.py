import configparser

config = configparser.ConfigParser()
config.read('secret_config.ini')

discord_settings = {
    'token': config.get('discord', 'token'),
    'bot': config.get('discord', 'bot'),
    'id': config.getint('discord', 'id'),
    'prefix': config.get('discord', 'prefix'),
    'debug': config.getboolean('discord', 'debug')
}

gsheets_settings = {
    'id': config.get('gsheets', 'id'),
    'film': config.get('gsheets', 'film')
}

vk = {
    'login': config.get('vk', 'login'),
    'password': config.get('vk', 'password')
}

CHESS_API_TOKEN = config.get('lichess', 'token')
