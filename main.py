import instaloader
import os

L = instaloader.Instaloader(download_comments=False, save_metadata=False)

username = input("username: ").strip()

output_dir = os.path.join("media", username)
os.makedirs(output_dir, exist_ok=True)

print(f"Downloading post from: {username}")
L.download_profile(username, profile_pic_only=False)
print(f"✅ Download complete file has been saved in: {output_dir}")