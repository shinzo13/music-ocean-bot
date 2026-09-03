YTM_DOMAIN = "https://music.youtube.com"
YTM_BASE_API = YTM_DOMAIN + "/youtubei/v1"
YT_DOMAIN = "https://www.youtube.com"
YT_BASE_API = YT_DOMAIN + "/youtubei/v1"
YTM_PARAMS = "?alt=json"
YTM_PARAMS_KEY = "&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"

HEADERS = {
    "user-agent": USER_AGENT,
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "content-type": "application/json",
    "content-encoding": "gzip",
    "origin": YTM_DOMAIN,
}

# Clients whose /player answers carry plain stream urls. Everything else gets a
# ciphered url that only the player javascript can unlock, or a bot check.
# Order is by how rarely youtube challenges them.
PLAYER_CLIENTS = (
    {
        "name": "VISIONOS",
        "id": 101,
        "ua": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 15_7_3) "
               "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 "
               "Safari/605.1.15"),
        "context": {
            "clientName": "VISIONOS",
            "clientVersion": "1.02",
            "deviceMake": "Apple",
            "deviceModel": "RealityDevice17,1",
            "osName": "visionOS",
            "osVersion": "26.5.23O471",
        },
    },
    {
        "name": "ANDROID_VR",
        "id": 28,
        "ua": ("com.google.android.apps.youtube.vr.oculus/1.65.10 "
               "(Linux; U; Android 12L; eureka-user Build/SQ3A.220605.009.A1) gzip"),
        "context": {
            "clientName": "ANDROID_VR",
            "clientVersion": "1.65.10",
            "deviceMake": "Oculus",
            "deviceModel": "Quest 3",
            "androidSdkVersion": 32,
            "osName": "Android",
            "osVersion": "12L",
        },
    },
)
