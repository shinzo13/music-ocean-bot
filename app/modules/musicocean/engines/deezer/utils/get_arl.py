from playwright.async_api import async_playwright
import asyncio

from app.config.log import get_logger
from app.config.settings import settings

logger = get_logger(__name__)

async def get_arl(email, password) -> str:
    logger.info("Getting Deezer ARL cookie via Playwright..")

    if settings.dev.enabled:
        # ZAGLUSHKA
        logger.info("Using saved ARL cookie (dev mode)")
        return settings.dev.arl

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        logger.debug("Launched browser")
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://account.deezer.com/login/")
        await page.wait_for_load_state("networkidle")
        logger.debug("Page loaded")
        await page.evaluate('document.getElementById("cookie-banner-deezer")?.remove()')
        await page.fill('input[id="email"]', email)
        await page.fill('input[id="password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        logger.debug("Submitted credentials")
        await asyncio.sleep(1)
        cookies = await context.cookies()
        arl_cookie = None
        for cookie in cookies:
            if cookie['name'] == 'arl':
                arl_cookie = cookie['value']
                break
        await browser.close()
        if arl_cookie:
            logger.info("Successfully fetched ARL cookie")
            return arl_cookie
        raise Exception("Error getting arl cookie") #TODO exception class