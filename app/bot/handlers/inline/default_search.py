from aiogram import Router, F
from aiogram.types import InlineQuery
from aiogram.types import InlineQueryResultAudio
from dishka import FromDishka

from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.bot.utils import generate_inline_results

router = Router()

@router.inline_query(F.query!="")
async def inline_query(
    query: InlineQuery,
    musicocean: FromDishka[TelegramMusicOceanClient]
):
    matches = await musicocean.search_tracks(query.query)
    await query.answer(generate_inline_results(matches))