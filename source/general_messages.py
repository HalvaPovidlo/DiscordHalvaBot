import secretConfig

px = secretConfig.discord_settings["prefix"]

HELP = "`" + px + "random` - проиграть случайную песню из таблицы\n" \
       "`" + px + "search` - выбрать все песни из таблицы по введенному слову\n" \
       "`" + px + "chess` - создать лобби на два игрока\n" \
       "`" + px + "sheet` - получить ссылку на таблицу с песнями\n" \
       "`" + px + "link` - все наши ссылки\n" \
       "`" + px + "youtube` - получить ссылки на наши youtube каналы с песнями\n" \
       "`" + px + "github` - получить ссылку на код бота в github\n" \
       "`" + px + "film` - получить ссылку на таблицу с фильмами\n" \
       "`" + px + "help` - чтобы увидеть это сообщение"

DIRTY_DETECTED = "С высокой вероятностью, вы являеетесь педофилом"

ANY_ERROR = "Произошла какая-то ошибка <:monkaS:817041877718138891>"

SHORT_REQUEST = "Напиши хотя бы 3 буквы <:PepeHands:817043023056994351>"

NEW_SONG = ["Новая песня добавлена <a:PepoDance:817043023149793361>",
            "Новая песня добавлена <a:catJAM:817043174840205312>"]

SHEET_LINK = "https://docs.google.com/spreadsheets/d/" + secretConfig.gsheets_settings['id'] + "/edit#gid=0"

GITHUB_LINK = "https://github.com/HalvaPovidlo/DiscordHalvaBot"

YOUTUBE = "https://www.youtube.com/channel/UC56_SqbimIM-j87hA1HF90A\n" \
          "https://www.youtube.com/channel/UCk2lvpg_bU6atRIKSUfWKUw"

YOUTUBE_1 = "https://www.youtube.com/channel/UC56_SqbimIM-j87hA1HF90A"

YOUTUBE_2 = "https://www.youtube.com/channel/UCk2lvpg_bU6atRIKSUfWKUw"

FILMS_LINK = "https://docs.google.com/spreadsheets/d/1yRudNo3YMm-FTTJRNJHcPCKBpUdC1URSZsjPNvfhff4/edit#gid=1519951860"


ALL_LINKS = "`Песни:` <" + SHEET_LINK + ">\n" \
       "`Гитхаб:` <" + GITHUB_LINK + ">\n" \
       "`Ютуб 1:` <" + YOUTUBE_1 + ">\n" \
       "`Ютуб 2:` <" + YOUTUBE_2 + ">\n" \
       "`Фильмы:` <" + FILMS_LINK + ">\n"
