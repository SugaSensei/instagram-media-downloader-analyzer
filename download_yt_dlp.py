import yt_dlp

def download_instagram_profile(username):
    url = f"https://www.instagram.com/{username}/"
    ydl_opts = {
        'download_archive': 'downloaded.txt',
        'match_filter': lambda info_dict: not info_dict.get('is_live', False),
        'outtmpl': f'downloads/{username}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    username = input("Instagram username: ").strip()
    download_instagram_profile(username)
