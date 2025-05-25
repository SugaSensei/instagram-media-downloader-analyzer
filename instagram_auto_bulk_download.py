import yt_dlp

INSTAGRAM_USERNAME = "rajx_sarwade"
profile_url = f"https://www.instagram.com/{INSTAGRAM_USERNAME}/"

ydl_opts = {
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "quiet": False,
    "noplaylist": True,
    "cookiefile": "cookies.txt",
    "force_generic_extractor": True,  # <-- add this line
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([profile_url])
