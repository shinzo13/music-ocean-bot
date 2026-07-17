from aiogram.types import InlineQueryResultArticle

from app.bot.utils.search_results import not_supported_result


def test_not_supported_result_structure():
    results = not_supported_result("Spotify playlist/artist link search")
    assert len(results) == 1
    article = results[0]
    assert isinstance(article, InlineQueryResultArticle)
    assert article.id == "not_supported"
