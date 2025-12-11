# User Agent
USERAGENT = "Mozilla/5.0 (X11; Linux i686; rv:135.0) Gecko/20100101 Firefox/135.0"

# HTTP Headers
HEADERS = {
    "User-Agent": USERAGENT,
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.deezer.com",
    "Referer": "https://www.deezer.com/login",
    "X-Requested-With": "XMLHttpRequest",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
}

# Endpoints
API_URL = "https://api.deezer.com"
USERDATA_URL = (
    "https://www.deezer.com/ajax/gw-light.php"
    "?method=deezer.getUserData"
    "&input=3"
    "&api_version=1.0"
    "&api_token="
)
ITEM_URL = "https://www.deezer.com/us/{type}/{id}"
MEDIA_URL = "https://media.deezer.com/v1/get_url"

# Regex Patterns
DATA_PATTERN = r"window\.__DZR_APP_STATE__\s*=\s*(\{.*?\})\s*<\s*/\s*script>"

# Format links
COVER_URL = "https://api.deezer.com/album/{album_id}/image"
