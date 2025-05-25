import os
import csv
import time
from instaloader import Instaloader, Post

# Optional: Use session cookies for private or logged-in access
USE_SESSION = False
USERNAME = 'your_username'
SESSIONFILE = 'session-your_username'

# Path to your CSV file
CSV_FILE = 'links.csv'

# Directory to save downloaded reels
DOWNLOAD_DIR = 'downloaded_reels'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize Instaloader
L = Instaloader(dirname_pattern=os.path.join(DOWNLOAD_DIR, '{shortcode}'), download_comments=False, save_metadata=False, post_metadata_txt_pattern="")

if USE_SESSION:
    try:
        L.load_session_from_file(USERNAME, SESSIONFILE)
    except FileNotFoundError:
        print("Session file not found. Logging in...")
        L.login(USERNAME, input("Enter your password: "))
        L.save_session_to_file(SESSIONFILE)

# Read URLs from CSV and process each
with open(CSV_FILE, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if not row:
            continue
        url = row[0].strip()
        if "/reel/" not in url:
            print(f"Skipping non-reel URL: {url}")
            continue
        try:
            shortcode = url.rstrip('/').split('/')[-1]
            post = Post.from_shortcode(L.context, shortcode)
            print(f"Downloading: {url}")
            L.download_post(post, target=shortcode)
            time.sleep(2)  # Be respectful to Instagram's servers
        except Exception as e:
            print(f"Failed to download {url}: {e}")
