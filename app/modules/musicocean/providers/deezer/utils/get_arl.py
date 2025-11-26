from playwright.async_api import async_playwright
import asyncio

async def get_arl(email, password):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://account.deezer.com/login/")
        await page.wait_for_load_state("networkidle")
        await page.evaluate('document.getElementById("cookie-banner-deezer")?.remove()')
        await page.fill('input[id="email"]', email)
        await page.fill('input[id="password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(1)
        cookies = await context.cookies()
        arl_cookie = None
        for cookie in cookies:
            if cookie['name'] == 'arl':
                arl_cookie = cookie['value']
                break
        await browser.close()
        if arl_cookie:
            return arl_cookie
        raise Exception("Error getting arl cookie") #TODO exception class