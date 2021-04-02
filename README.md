# DiscordHalvaBot

## Join all our teams

Email me at andrei.khodko@gmail.com to be added to the [Discord Developer Portal](https://discord.com/developers/applications) and [Google API Console](https://console.developers.google.com) teams.

## Enable Discord

You need to sign up at [Discord Developer Portal](https://discord.com/developers/applications)

And join our HPDevelopment team.

Create file `source/secretConfig.py`

```
discord_settings = {
    'token': '***',
    'bot': 'HalvaBot',
    'id': 746726055259406426,
    'prefix': '$',
    'debug': True
}

gsheets_settings = {
    'id': '***',
    'film': '***'
}
```
Replace `token` with token from Discord Developer Portal.

Applications -> HalvaBot -> Bot -> Click to reveal token

**Don't pass this token on to anyone!!!**

## Enable Google Sheets

In `secretConfig.py` replace `gsheets_settings.id` with the id of our table.

Sign in to [Google API Console](https://console.developers.google.com) 

Credentials -> OAuth client -> DOWNLOAD JSON

Move the json file to `source/music_manager/` and rename it to `credentials.json`.

Run `main.py`.

## Documentation

https://discordpy.readthedocs.io/en/latest/api.html
