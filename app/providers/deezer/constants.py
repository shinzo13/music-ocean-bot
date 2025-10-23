USERAGENT = "Mozilla/5.0 (X11; Linux i686; rv:135.0) Gecko/20100101 Firefox/135.0"
headers = {
    'Pragma': 'no-cache',
    'Origin': 'https://www.deezer.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': USERAGENT,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://www.deezer.com/login',
    'DNT': '1',
}
API_URL = "https://api.deezer.com"
SEARCH_API_URL = "https://api.deezer.com/search/{}?q={}"
USERDATA_URL = "https://www.deezer.com/ajax/gw-light.php?method=deezer.getUserData&input=3&api_version=1.0&api_token="
ITEM_URL = "https://www.deezer.com/us/{}/{}"
DATA_PATTERN = r"window\.__DZR_APP_STATE__\s*=\s*(\{.*?\})\s*<\s*/\s*script>"

