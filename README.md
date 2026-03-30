# Music Ocean Bot

---

<img src="https://img.shields.io/badge/python-3.12-blue?logo=python" />
<img src="https://img.shields.io/badge/aiogram-3.x-2CA5E0?logo=telegram" />
<img src="https://img.shields.io/badge/status-WIP-orange" />

Telegram inline-moded bot for fast searching & downloading music from different sources.

Project demo: [@koshke2bot](koshke2bot.t.me)

## Features
- Supported musical services: **Spotify**, **YTMusic**, **SoundCloud**, **Deezer**.
- **Last.fm scrobbling** _(beta)_: instantly downloading the track user is listening to.
- Entity searching: search **tracks**, **albums**, **artists** or even **playlists**.
- **Database cache**: once any track downloaded, it can be easily accessed again without repeating the download.
- **ID3 tags** support: all downloaded media has proper ready-to-go ID3 tags.
- 

## Installation
```bash
cp .env.example .env
# fill the .env file
```

Here is some notes about several `.env` variables:


| Variable | Description                                                                                                                                |
|---|--------------------------------------------------------------------------------------------------------------------------------------------|
| `LOGGING__LEVEL` | _Logging level. `INFO` for default._                                                                                                       |
| `TRACKS__WATERMARK` | _Optional. String watermark that will be injected in all the downloaded media_                                                             |
| `BOT__TOKEN` | _Telegram bot token. Can be obtained via [@BotFather](https://t.me/BotFather)._                                                            |
| `SERVER__DOMAIN` | _Domain of the server that is being used as endpoint._                                                                                     |
| `SERVER__CERTFILE_PATH` | _Path to the certificate file on your host._                                                                                               |
| `TELEGRAM__ADMINS` | _List of Telegram ID's of users being administrators._                                                                                     |
| `TELEGRAM__CHANNEL_ID` | _Telegram ID of the channel that will act like media database._                                                                            |
| `TELEGRAM__WORKERS` | _Optional. List of Telegram ID's of bots that will help the main one with downloading media._                                              |
| `DEEZER__LOGIN` | _[Deezer](deezer.com) account login_                                                                                                       |
| `DEEZER__PASSWORD` | _[Deezer](deezer.com) account password_                                                                                                    |
| `SPOTIFY__CLIENT_ID` | _`client_id` of registered Spotify app. Can be obtained on [Spotify for Developers](https://developer.spotify.com/dashboard) dashboard._   |
| `SPOTIFY__CLIENT_SECRET` | _`client_secret` of registered Spotify app. Can be obtained on [Spotify for Developers](https://developer.spotify.com/dashboard) dashboard._ |


### Running application:
```bash
# заполни .env
docker compose up --build
```

## Usage

### User manual
Bot's main menu accessed via `/start` command. `Profile` and `Settings` tabs can be found there. 

In order to search music, just write `@botname <YOUR QUERY>` in the message input field.

There are several available search options:
- **Default search**: `@botname <TRACK QUERY>`, ex. `@koshke2bot Back in black`
- **Engine-specified search**: `@botname <dz/sc/yt/sp> <QUERY>`, ex. `@koshke2bot dz:goth tv`
- **Entity search**: `@botname <album/artist/playlist> <QUERY>`, ex. `@koshke2bot album:Who really cares` or just `@koshke2bot al:Who really cares`
- **Combined search**: you can combine engine and entity specification, ex. `@koshke2bot sc:pl:Jazz`
- **In-entity search**: automatically pasted via `Search tracks` button, looks like `@botname al_id:1ch95c`. Do not modify it!

In the `Settings` tab, you can set up following options:
- **Default engine** used to search and download music
- **Track previews** that can appear as _album covers_ as well as _MP3-previews_
- **Last.fm scrobbling**: you can connect your Spotify & Last.fm accounts in order to instantly download music you are listening now to / listened recently.

### Administrating manual

`Admin panel` is accessible via main menu for users with administrator rights. There you cand find:
- Downloading users database as `.csv`
- Editing users rights / banning users
- Mailing
- Bot usage statistics

The other admin tool available is getting the track info. Simply send downloaded media to the bot to get information about who, when and how downloaded it.

