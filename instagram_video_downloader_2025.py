import asyncio
import yt_dlp
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import random
import time
import logging
import json  # ← Add this at the top of your script


INSTAGRAM_USERNAME = "rajx_sarwade"
PROFILE_URL = f"https://www.instagram.com/{INSTAGRAM_USERNAME}/"
MAX_SCROLLS = 20      # Adjust max scrolls to control how many posts you load

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.FileHandler("insta_downloader.log"),
                              logging.StreamHandler()])

async def run_playwright():
    logging.info(f"Starting Playwright browser for {PROFILE_URL}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        # Load cookies from file
        try:
            with open("cookies.json", "r") as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            # Playwright expects list of dict cookies; use playwright's cookie parser or your own conversion if needed
            # Here you might want to parse Netscape format or convert it to JSON cookies manually
            # For simplicity, let's assume cookies.json is Playwright-compatible cookies (better)
            # So instead, save cookies in Playwright JSON format or manually set cookies:
            # OR skip this step and login manually once, then save storage state
            # For now skipping cookie load for brevity
        except Exception as e:
            logging.warning(f"Could not load cookies.txt: {e}")

        page = await context.new_page()
        await stealth_async(page)

        logging.info("Navigating to profile page...")
        await page.goto(PROFILE_URL, wait_until="networkidle")

        post_urls = set()
        last_height = await page.evaluate("() => document.body.scrollHeight")

        scrolls = 0
        while scrolls < MAX_SCROLLS:
            # Extract posts URLs visible on the page
            anchors = await page.query_selector_all("article a[href*='/p/'], article a[href*='/reel/']")
            for a in anchors:
                href = await a.get_attribute("href")
                full_url = f"https://www.instagram.com{href}"
                post_urls.add(full_url)
            logging.info(f"Scroll {scrolls+1}: Found {len(post_urls)} unique posts so far.")

            # Scroll down slowly with randomized delay
            await page.evaluate("window.scrollBy(0, window.innerHeight);")
            await asyncio.sleep(random.uniform(1.5, 3.5))

            new_height = await page.evaluate("() => document.body.scrollHeight")
            if new_height == last_height:
                logging.info("Reached bottom of page or no more posts to load.")
                break
            last_height = new_height
            scrolls += 1

        await browser.close()
        return list(post_urls)

def download_post(url, ydl_opts):
    logging.info(f"Downloading post: {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            logging.error(f"Failed to download {url}: {e}")

async def main():
    posts = await run_playwright()

    if not posts:
        logging.error("No posts found, exiting.")
        return

    ydl_opts = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": False,
        "cookiefile": "cookies.txt",  # Make sure this is Playwright/yt-dlp compatible cookies for auth
        "nooverwrites": True,
        "retries": 3,
        "continuedl": True,
        "format": "bestvideo+bestaudio/best",
    }

    for url in posts:
        download_post(url, ydl_opts)
        # Random delay to avoid bot detection
        time.sleep(random.uniform(2, 5))

if __name__ == "__main__":
    asyncio.run(main())
