import secretConfig
px = secretConfig.discord_settings["prefix"]
HELP = "`" + px + "random` - проиграть случайную песню из таблицы\n" \
       "`" + px + "sheet` - получить ссылку на таблицу с песнями\n" \
       "`" + px + "guide` - чтобы увидеть это сообщение"

DIRTY_DETECTED = "С высокой вероятностью, вы являеетесь педофилом"

SONG_ERROR = "Произошла какая-то ошибка monkaS"

NEW_SONG = "Новая песня добавлена peepoDance"

SHEET_LINK = "https://docs.google.com/spreadsheets/d/" + secretConfig.gsheets_settings['id'] + "/edit#gid=0"
