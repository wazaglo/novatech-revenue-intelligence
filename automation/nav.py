import asyncio, os
from playwright.async_api import async_playwright

SHOTS = "/home/wazaglo/udacity/deliverables/screenshots"

async def connect():
    pw = await async_playwright().start()
    browser = await pw.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0] if browser.contexts else await browser.new_context(viewport={"width": 1600, "height": 900})
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    return pw, browser, ctx, page

async def shot(page, name, full=False):
    os.makedirs(SHOTS, exist_ok=True)
    path = os.path.join(SHOTS, name + ".png")
    await page.screenshot(path=path, full_page=full)
    print("shot:", path)
    return path

async def settle(page, ms=1500):
    await page.wait_for_timeout(ms)
