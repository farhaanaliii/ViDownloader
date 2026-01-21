# ViDownloader

<p align="center">
  <img src="vidownloader/icons/icon.png" alt="ViDownloader Logo" width="128" height="128">
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-orange.svg)](https://github.com/farhaanaliii/vidownloader)
[![PyPI Version](https://img.shields.io/pypi/v/vidownloader?color=blue)](https://pypi.org/project/vidownloader/)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/farhaanaliii/vidownloader/releases)
[![Built with PyQt5](https://img.shields.io/badge/Built%20with-PyQt5-green.svg)](https://www.qt.io/)
[![Powered by yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

> [!WARNING]
> **Heads up**: This is currently in **Beta** phase. It works, but there might be rough edges and unexpected behavior. Your feedback will help shape the stable release.

<p align="center">
  <img src="assets/image1.png" alt="ViDownloader Screenshot">
</p>

---

## What This Is

ViDownloader is a desktop application built with PyQt5 that simplifies downloading YouTube videos in bulk. While it uses **yt-dlp** under the hood for the actual downloading, the scraping and interface are completely custom-built.

This happens to be my first substantial open-source project, so please bear with me. it might do some dumb things, but I'm learning as I go. If something breaks or doesn't make sense, let me know and I'll do my best to fix it.

---

## Quick Start

### Install via pip (PyPI)

```bash
pip install vidownloader
```

### Or from source

```bash
git clone https://github.com/farhaanaliii/vidownloader.git
cd vidownloader
pip install -e .
```

### Launch the App

After installation, run:

```bash
vidownloader
```

Or, if you prefer:

```bash
python -m vidownloader
```

---

## What You Can Download

Paste almost any YouTube URL and ViDownloader will figure out the rest:

- **Channel videos** – `https://youtube.com/@channel/videos`
- **Channel shorts** – `https://youtube.com/@channel/shorts`
- **Playlist videos** – `https://youtube.com/playlist?list=PLAYLIST_ID`
- **Single videos** – `https://youtube.com/watch?v=VIDEO_ID`
- **Single shorts** – `https://youtube.com/shorts/VIDEO_ID`

Just paste one or more links (one per line) and let the app handle the scraping and downloading.

---

## How It Works

1. **Paste Links** – Add YouTube URLs into the text area
2. **Scrape Metadata** – Click *Start* to fetch video details using custom scraping logic
3. **Select Videos** – Choose which videos you want from the list
4. **Download** – Hit *Download* and let **yt-dlp** do its magic in the background

The interface sits on top of **yt-dlp** for reliable downloads, but all the scraping, queuing, and progress tracking happens within ViDownloader itself.

---

## Configuration

Open **Settings** (top-right corner) to adjust:

| Setting | What It Does |
|---------|--------------|
| **Download Location** | Where your videos are saved |
| **Export Location** | Where `.viio` list files are stored |
| **File Naming** | Name files by title, video ID, or random string |
| **Download Threads** | Simultaneous downloads (1–10 threads) |

---

## Export & Resume

Working with a large channel? Export your video list as a `.viio` file, close the app, and import it later to resume right where you left off. No need to re-scrape everything.

---

## System Requirements

- **Python 3.9** or newer
- **PyQt5** (≥ 5.15.11)
- **yt-dlp** (latest recommended)
- **curl_cffi**
- **FFmpeg** – Required by yt-dlp for video/audio processing ([download](https://github.com/yt-dlp/FFmpeg-Builds/releases/tag/latest))
- **JavaScript Runtime** – yt-dlp needs a JS engine to handle some videos. Install one of:
  - [Deno](https://deno.land/)
  - [Node.js](https://nodejs.org/)
  - [Bun](https://bun.sh/)

Python dependencies install automatically via `pip`. You'll need to install FFmpeg and a JS runtime separately.

> [!TIP]
> **One-click installer coming soon!** A standalone installer that bundles all dependencies is in development.

---

## Cross-Platform Support

ViDownloader is **cross-platform** and has been tested on:

- **Windows** (10, 11)
- **Linux** (Ubuntu 22.04)

The application is built with Python and PyQt5, making it portable across different operating systems. Both the source installation and pre-built executables work seamlessly on supported platforms.

---

## Building Executables

Want to build a standalone executable? Use the provided build scripts:

**Windows:**
```powershell
.\build.bat
```

**Linux:**
```bash
./build.sh
```

These scripts will automatically:
- Set up the virtual environment
- Install dependencies
- Compile Qt resources
- Build the executable using Nuitka

Pre-built executables are also available for download:

- **Windows** (x86/x64)
- **Linux** (x64)

Check the [Releases](https://github.com/farhaanaliii/vidownloader/releases) page for downloads.

---

## Development & Contribution

This is my first major open-source project, so I'm sure there are plenty of areas to improve. If you find bugs, have feature ideas, or want to contribute code:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

All contributions are welcome. just try to match the existing code style.

---

## License

Released under the **[MIT License](https://opensource.org/licenses/MIT)**. Use it, modify it, share it.

---

## Coming Soon

- **Format & quality selection** – Pick 720p, 1080p, 4K, etc.
- **Advanced filtering** – Search and filter video lists
- **Download history** – Track your past downloads
- **Improved error handling** – Making the app more resilient

> **TODO**: If you're good with design, we could really use a better logo. The current one is... functional, but not pretty. Any takers?

---

## Acknowledgment

While ViDownloader implements its own scraping logic, it relies on the excellent **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** project for actual video downloading. Big thanks to the yt-dlp maintainers for their incredible work.

---

## Author

Built by **[Farhan Ali](https://github.com/farhaanaliii)** – my first serious dive into open-source desktop apps. Be gentle.
