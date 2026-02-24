import time


def initialize_context() -> dict:
    return {
        "context": {
            "client": {
                "clientName": "WEB_REMIX",
                "clientVersion": "1." + time.strftime("%Y%m%d", time.gmtime()) + ".01.00",
                "hl": "en"
            },
            "user": {},
        }
    }