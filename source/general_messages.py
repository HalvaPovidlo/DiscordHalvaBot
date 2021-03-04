import secretConfig
px = secretConfig.discord_settings["prefix"]
HELP = "`" + px + "random` - проиграть случайную песню из таблицы\n" \
       "`" + px + "search` - выбрать все песни из таблицы по введенному слову\n" \
       "`" + px + "sheet` - получить ссылку на таблицу с песнями\n" \
       "`" + px + "github` - получить ссылку на код бота в github\n" \
       "`" + px + "guide` - чтобы увидеть это сообщение"

DIRTY_DETECTED = "С высокой вероятностью, вы являеетесь педофилом"

SONG_ERROR = "Произошла какая-то ошибка <:monkaS:817041877718138891>"

SHORT_REQUEST = "Напиши хотя бы 3 буквы <:PepeHands:817043023056994351>"

NEW_SONG = "Новая песня добавлена <a:PepoDance:817043023149793361>"

SHEET_LINK = "https://docs.google.com/spreadsheets/d/" + secretConfig.gsheets_settings['id'] + "/edit#gid=0"

GITHUB_LINK = "https://github.com/HalvaPovidlo/DiscordHalvaBot"
