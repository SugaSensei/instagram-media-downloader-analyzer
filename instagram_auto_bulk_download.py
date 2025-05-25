# instagram_auto_bulk_download.py

import time
import requests
from bs4 import BeautifulSoup
import browsercookie
import yt_dlp

INSTAGRAM_USERNAME = "rajx_sarwade"

def get_headers_from_cookies_txt():
    with open("cookies.txt", "r") as f:
        cookies_raw = f.read()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": ""
    }

    cookies = []
    for line in cookies_raw.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.strip().split("\t")
        if len(parts) == 7:
            cookies.append(f"{parts[5]}={parts[6]}")
    headers["Cookie"] = "; ".join(cookies)
    return headers

def get_post_links(username):
    print(f"Fetching posts for @{username}...")
    base_url = f"https://www.instagram.com/{username}/"
    headers = get_headers_from_cookies_txt()
    r = requests.get(base_url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    shared_data_script = next(
        (s for s in soup.find_all("script") if "window._sharedData" in s.text),
        None
    )

    if not shared_data_script:
        raise Exception("Could not find shared data script!")

    json_text = shared_data_script.string.split(" = ", 1)[1].rstrip(";")
    import json
    data = json.loads(json_text)

    posts = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
    post_urls = [f"https://www.instagram.com/p/{post['node']['shortcode']}/" for post in posts]
    return post_urls

def download_posts(post_urls):
    print(f"Found {len(post_urls)} posts. Downloading...")
    ydl_opts = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": False,
        "noplaylist": True,
        "cookiefile": "cookies.txt",  # 👈 auto-uses cookies!
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in post_urls:
            try:
                print(f"Downloading {url}")
                ydl.download([url])
            except Exception as e:
                print(f"❌ Failed to download {url}: {e}")

if __name__ == "__main__":
    posts = get_post_links(INSTAGRAM_USERNAME)
    download_posts(posts)
