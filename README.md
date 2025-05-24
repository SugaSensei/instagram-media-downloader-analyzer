# instagram-media-downloader-analyzer

A powerful, extensible tool to download and analyze Instagram media — Reels, Images, and Videos — directly from public Instagram page links. It stores each post's metadata including captions, hashtags, post timing, tags, likes, views, comments, and more — making it ideal for studying content trends, engagement, and Instagram’s algorithm.

---

## 📌 Features

- 🔗 Download all posts from an Instagram page using its URL
- 🎞️ Choose between: only Reels, only Images, or both
- 📥 Save each video as `.mp4` and its corresponding caption as `.txt`
- 🏷️ Extract hashtags, mentions, and post metadata (likes, comments, time, etc.)
- 📊 Designed for future analytics and Instagram growth insights
- 💾 All files saved with meaningful names for easy navigation

---

## 🚀 Usage (Coming Soon)
1. Clone the repo
2. Install dependencies
3. Run the script and input the Instagram page URL
4. Choose content type to download (Reels, Images, or Both)

---

## 🛠️ Tech Stack

- Python 3.10+
- [Instaloader](https://instaloader.github.io/)
- (Planned) Pandas, SQLite, Matplotlib for data analysis

---

## 🧱 Folder Structure

```
instagram-media-downloader-analyzer/
├── reels/
│   ├── reel1.mp4
│   ├── reel1.txt
├── images/
│   ├── image1.jpg
│   ├── image1.txt
├── download_instagram_media.py
├── requirements.txt
└── README.md
```

---

# ✅ POC (Proof of Concept)

## Objective:
Demonstrate the technical possibility to:
- Download posts (Reels, Images, Videos) from a public Instagram page
- Filter by media type
- Save media and metadata properly

## Tech Stack:
- Python 3.10+
- Instaloader
- Native file operations

## Deliverables:
- Media files (`.mp4`, `.jpg`)
- Captions and metadata saved as `.txt` and `.csv`

## Limitations:
- Public accounts only (or with login)
- Rate-limiting by Instagram may apply

---

# ✅ PRD (Product Requirements Document)

## 🎯 Purpose
To build a tool that helps users download and analyze media from Instagram pages to understand engagement, trends, and the Instagram algorithm.

## 👤 Target Audience
- Content Creators
- Social Media Analysts
- Digital Marketers
- Python Learners

## 📋 Functional Requirements

| ID | Feature | Description |
|----|---------|-------------|
| F1 | Input IG page URL | User inputs IG username or link |
| F2 | Media filter | Choose Reels, Images, or Both |
| F3 | Download media | Save `.mp4`, `.jpg` files locally |
| F4 | Metadata extract | Save caption, hashtags, time, etc. |
| F5 | Save as text | `.txt` file per post |
| F6 | CSV/JSON export | Store all metadata for analysis |
| F7 | Extract comments | Top comments stored (if enabled) |
| F8 | Store stats | Likes, Views, Comments |
| F9 | Future growth | Ready for analytics & ML insights |

## 🧰 Non-functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| N1 | Usability | CLI interface, beginner-friendly |
| N2 | Portability | Cross-platform compatibility |
| N3 | Extensibility | Modular code design |
| N4 | Performance | Efficient download of 100+ posts |

---

## 📆 7-Day Milestone Plan

| Day | Task | Outcome |
|-----|------|---------|
| Day 1 | Setup project, folder, requirements | Working base |
| Day 2 | Basic media download (filter: Reels, Images, Both) | Core downloader done |
| Day 3 | Caption + metadata extraction | `.txt` with caption & tags |
| Day 4 | CSV/JSON export of metadata | Structured dataset |
| Day 5 | Add engagement metrics | Likes, comments, views |
| Day 6 | Analytics + summary export | Bar chart or top posts |
| Day 7 | Polish, test, final README & demo | Ready for showcase ✅ |

---

## 📈 Future Enhancements

- SQLite database integration
- Trend and hashtag performance analysis
- GUI using Tkinter or Electron
- Auto-scheduled scraping and updates
- Multi-user support and login

---

## 🧠 Learning Path (Kaizen Style)

This project follows the Kaizen philosophy — consistent daily progress to master Python and build a real-world portfolio-worthy tool.

---

## 🤝 Contributing

Fork this repo, submit PRs, and help expand the toolkit!

## 📜 License

MIT License

---

## 🔗 Inspired By

This tool was inspired by the need to understand Instagram growth and automate repetitive media analysis — for creators, analysts, and students alike.
