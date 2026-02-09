
import asyncio, time
from playwright.async_api import async_playwright
from collectors.common.robots_guard import allowed_to_fetch

AGENT = "JobIntelBot/1.0 (+contact@example.com)"

async def collect_company_jobs(listing_url: str, robots_url: str):
    if not allowed_to_fetch(robots_url, AGENT, listing_url):
        raise RuntimeError("robots.txt forbids crawling this path")
    jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=AGENT)
        await page.goto(listing_url, wait_until="domcontentloaded")
        cards = page.locator(".job-card")  # update selector per site
        n = await cards.count()
        for i in range(n):
            title = (await cards.nth(i).locator(".title").inner_text()).strip()
            href = await cards.nth(i).locator("a").get_attribute("href")
            url = await page.evaluate("(h) => new URL(h, document.baseURI).toString()", href)
            jobs.append({"title": title, "url": url})
            await page.wait_for_timeout(300)
        await browser.close()
    time.sleep(0.25)
    return jobs
