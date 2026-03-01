import ssl
from aiohttp import web
from dishka.integrations.aiohttp import FromDishka

from app.config import settings
from app.config.log import get_logger
from app.database.repositories import UserRepository, DynamicSettingsRepository

logger = get_logger(__name__)

router = web.RouteTableDef()

@router.get('/spotify')
async def spotify_callback(
        request: web.Request,
        user_repo: FromDishka[UserRepository],
        dynamic_settings_repo: FromDishka[DynamicSettingsRepository],
):
    code = request.rel_url.query.get("code")
    state = request.rel_url.query.get("state")

    if not code or not state:
        return web.Response(status=400)

    user = await user_repo.update_user_settings(
        user_id=int(state),
        spotify__connection_code=code
    )

    logger.debug(f"{user=}")

    bot_username = (await dynamic_settings_repo.get()).bot_username
    raise web.HTTPFound(location=f"https://t.me/{bot_username}?start=spotify_connected")

app = web.Application()
app.add_routes(router)

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(
    settings.server.certfile_path,
    settings.server.keyfile_path
)