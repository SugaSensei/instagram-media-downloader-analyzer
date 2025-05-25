import asyncio
import json
import logging
import random
from pathlib import Path
from playwright.async_api import async_playwright

PROFILE_URL = "https://www.instagram.com/rajx_sarwade/"
MAX_SCROLLS = 10  # max scroll attempts to load posts
COOKIES_FILE = "cookies.json"  # external cookie file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def load_cookies(file_path: str):
    path = Path(file_path)
    if not path.is_file():
        logging.error(f"Cookies file '{file_path}' not found.")
        return []
    with path.open("r", encoding="utf-8") as f:
        cookies = json.load(f)
    return cookies

async def main():
    cookies = await load_cookies(COOKIES_FILE)
    if not cookies:
        logging.error("No cookies loaded, exiting.")
        return

    async with async_playwright() as p:
        logging.info(f"Starting Playwright browser for {PROFILE_URL}")
        browser = await p.chromium.launch(headless=False)  # set to True for no UI
        context = await browser.new_context()

        await context.add_cookies(cookies)
        logging.info("Cookies loaded into browser context.")

        page = await context.new_page()
        await page.goto(PROFILE_URL, wait_until="networkidle")
        await page.wait_for_timeout(5000)

        post_urls = set()
        last_height = await page.evaluate("() => document.body.scrollHeight")
        scrolls = 0

        while scrolls < MAX_SCROLLS:
            anchors = await page.query_selector_all("a[href^='/p/'], a[href^='/reel/']")
            if not anchors:
                logging.warning("No post links found during this scroll.")

            for a in anchors:
                href = await a.get_attribute("href")
                if href and href not in post_urls:
                    full_url = f"https://www.instagram.com{href}"
                    post_urls.add(full_url)

            logging.info(f"Scroll {scrolls + 1}: Found {len(post_urls)} unique posts so far.")

            await page.evaluate("window.scrollBy(0, window.innerHeight);")
            await asyncio.sleep(random.uniform(2, 4))

            new_height = await page.evaluate("() => document.body.scrollHeight")
            if new_height == last_height:
                logging.info("Reached end of page or no more posts to load.")
                break
            last_height = new_height
            scrolls += 1

        if not post_urls:
            logging.error("No posts found. Exiting.")
            await browser.close()
            return

        logging.info(f"Total posts found: {len(post_urls)}")
        for url in post_urls:
            logging.info(f"Post URL: {url}")

        # Add your download logic here

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
