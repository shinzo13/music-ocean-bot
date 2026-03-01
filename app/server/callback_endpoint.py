import ssl
from aiohttp import web
from dishka.integrations.aiohttp import FromDishka

from app.config import settings
from app.database.repositories import UserRepository

router = web.RouteTableDef()

@router.get('/spotify')
async def spotify_callback(
        request: web.Request,
        user_repo: FromDishka[UserRepository]
):
    code = request.rel_url.query.get("code")
    state = request.rel_url.query.get("state")

    if not code or not state:
        return web.Response(status=400)

    await user_repo.update_user_settings(
        user_id=int(state),
        spotify__connection_code=code
    )

    bot_username = settings.bot.username
    raise web.HTTPFound(location=f"https://t.me/{bot_username}?start=spotify_connected")

app = web.Application()
app.add_routes(router)

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(
    settings.server.certfile_path,
    settings.server.keyfile_path
)