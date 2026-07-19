import os

# app.config.settings instantiates Settings() at import time; on CI there is
# no .env, so collection dies. dummy values keep unit tests importable
_DUMMY_ENV = {
    "DEV__ENABLED": "false",
    "DEV__ARL": "x",
    "DEV__CLIENT_ID": "x",
    "LOGGING__LEVEL": "INFO",
    "BOT__TOKEN": "1:x",
    "SERVER__DOMAIN": "localhost",
    "SERVER__CERTFILE_PATH": "/dev/null",
    "SERVER__KEYFILE_PATH": "/dev/null",
    "TELEGRAM__ADMINS": "[1]",
    "TELEGRAM__CHANNEL_ID": "-100",
    "TELEGRAM__WORKERS": '["1:x"]',
    "DEEZER__LOGIN": "x",
    "DEEZER__PASSWORD": "x",
    "SPOTIFY__CLIENT_ID": "x",
    "SPOTIFY__CLIENT_SECRET": "x",
    "YANDEX__TOKEN": "x",
    "LASTFM__API_KEY": "x",
    "DATABASE__USER": "x",
    "DATABASE__PASSWORD": "x",
    "DATABASE__DB": "x",
    "LOCAL__WATERMARK": "",
    "LOCAL__GUIDE_URL": "",
}

for key, value in _DUMMY_ENV.items():
    os.environ.setdefault(key, value)
