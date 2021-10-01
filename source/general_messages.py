import secretConfig

px = secretConfig.discord_settings["prefix"]

HELP = "`" + px + "random` - проиграть случайную песню из таблицы\n" \
       "`" + px + "search` - выбрать все песни из таблицы по введенному слову\n" \
       "`" + px + "chess` - создать лобби на два игрока\n" \
       "`" + px + "sheet` - получить ссылку на таблицу с песнями\n" \
       "`" + px + "link` - все наши ссылки\n" \
       "`" + px + "recommend` - получить рекомендации на основе таблицы фильмов Халвы\n" \
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

YOUTUBE_DANGERZONE = "https://www.youtube.com/channel/UC56_SqbimIM-j87hA1HF90A"

YOUTUBE_PIPIBIBA = "https://www.youtube.com/channel/UCk2lvpg_bU6atRIKSUfWKUw"

YOUTUBE_HALVA = "https://www.youtube.com/channel/UCr8LVDMr0pdslRm8SzQ23Sg"

FILMS_LINK = f"https://docs.google.com/spreadsheets/d/{secretConfig.gsheets_settings['film']}/edit#gid=1519951860"


ALL_LINKS = "`Песни:` <" + SHEET_LINK + ">\n" \
       "`github:` <" + GITHUB_LINK + ">\n" \
       "`DronInTheDangerZone :` <" + YOUTUBE_DANGERZONE + ">\n" \
       "`пипибиба:` <" + YOUTUBE_PIPIBIBA + ">\n" \
       "`DiscordHalva Music:` <" + YOUTUBE_HALVA + ">\n" \
       "`Фильмы:` <" + FILMS_LINK + ">\n"
