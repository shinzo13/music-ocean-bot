from aiohttp import web
from dishka.integrations.aiohttp import FromDishka

from app.database.repositories import UserRepository

router = web.RouteTableDef()

@router.get('/spotify/callback')
async def spotify_callback(
        request: web.Request,
        user_repo: FromDishka[UserRepository]
):
    code = request.rel_url.query.get("code")
    state = request.rel_url.query.get("state")  # tg_user_id

    if not code or not state:
        return web.Response(status=400, text="Missing code or state")

    await user_repo.update_user_settings(
        user_id=int(state),
        spotify__connection_code=code
    )

    raise web.HTTPFound(location="https://t.me/mybot?start=spotify_connected")

app = web.Application()
app.add_routes(router)