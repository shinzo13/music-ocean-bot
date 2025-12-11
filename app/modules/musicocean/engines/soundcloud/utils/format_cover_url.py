def format_cover_url(url: str | None) -> str | None:
    if not url:
        # return None # TODO idk what to choose
        return "https://soundcloud.com/images/default_avatar_large.png"
    return url.replace("large", "t300x300")
