<div align="center">

# ViDownloader

<img src="https://raw.githubusercontent.com/farhaanaliii/ViDownloader/main/assets/icon.svg" alt="ViDownloader Logo" width="128" height="128">

A PySide6 desktop app for bulk downloading YouTube videos.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-orange.svg?style=flat-square)](https://github.com/farhaanaliii/vidownloader)
[![PyPI Version](https://img.shields.io/pypi/v/vidownloader?color=blue&style=flat-square)](https://pypi.org/project/vidownloader/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D4.svg?style=flat-square&logo=windows&logoColor=white)](https://github.com/farhaanaliii/vidownloader/releases)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52.svg?style=flat-square&logo=qt&logoColor=white)](https://www.qt.io/)
[![yt-dlp](https://img.shields.io/badge/Backend-yt--dlp-FF0000.svg?style=flat-square&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)

</div>

---

> [!WARNING]
> **Heads up**: This is currently in **Beta** phase. It works, but there might be rough edges and unexpected behavior. Your feedback will help shape the stable release.

![ViDownloader Screenshot](https://github.com/farhaanaliii/ViDownloader/raw/main/assets/image1.png)

---

## What This Is

ViDownloader is a desktop application built with PySide6 that simplifies downloading YouTube videos in bulk. While it uses **yt-dlp** under the hood for the actual downloading, the scraping and interface are completely custom-built.

This happens to be my first substantial open-source project, so please bear with me. it might do some dumb things, but I'm learning as I go. If something breaks or doesn't make sense, let me know and I'll do my best to fix it.

---

## Quick Start

### Install via pip

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

- **Channel videos** - `https://youtube.com/@channel/videos`
- **Channel shorts** - `https://youtube.com/@channel/shorts`
- **Playlist videos** - `https://youtube.com/playlist?list=PLAYLIST_ID`
- **Single videos** - `https://youtube.com/watch?v=VIDEO_ID`
- **Single shorts** - `https://youtube.com/shorts/VIDEO_ID`

Just paste one or more links (one per line) and let the app handle the scraping and downloading.

---

## How It Works

1. **Paste Links** - Add YouTube URLs into the text area
2. **Scrape Metadata** - Click Start to fetch video details using custom scraping logic
3. **Select Videos** - Choose which videos you want from the list
4. **Download** - Hit Download and let yt-dlp do its magic in the background

The interface sits on top of yt-dlp for reliable downloads, but all the scraping, queuing, and progress tracking happens within ViDownloader itself.

---

## Features

- **Bulk downloads** - Scrape entire channels, playlists, or mixed link lists
- **Multi-threaded** - Run 1 to 10 simultaneous downloads
- **Pause & Resume** - Pause active downloads and resume them at any time
- **Real-time progress** - Per-video progress bars, status indicators, file size display, and duration
- **Right-click shortcuts** - Play downloaded videos directly in your player, show files in Explorer, or copy links
- **Browser cookies support** - Extract cookies directly from your browser or profile for authenticated downloads
- **Export & Import** - Save your video list as a `.viio` file and reload it later without re-scraping
- **Flexible file naming** - Name files by video title, video ID, or a random string
- **Flexible organization** - Organize downloads by playlist name, uploader, or into a dedicated singles folder

---

## Configuration

Open **Settings** (top-right corner) to adjust:

| Setting | What It Does |
|---|---|
| **Download Location** | Where your videos are saved |
| **Export Location** | Where `.viio` list files are stored |
| **File Naming** | Name files by title, video ID, or random string |
| **Download Threads** | Simultaneous downloads (1 to 10 threads) |
| **Playlist Organization** | Group by playlist name or by uploader |
| **Single Video Organization** | Group in a singles folder or by uploader |
| **Cookies Browser & Profile** | Extract cookies from browser or profile for authenticated downloads |

---

## Export & Resume

Working with a large channel? Export your video list as a `.viio` file, close the app, and import it later to resume right where you left off. No need to re-scrape everything.

---

## System Requirements

- **Python 3.10** or newer
- **PySide6** (>= 6.5.0)
- **yt-dlp** (latest recommended)
- **curl_cffi**
- **FFmpeg** - Required by yt-dlp for video/audio processing ([download](https://github.com/yt-dlp/FFmpeg-Builds/releases/tag/latest))
- **JavaScript Runtime** - yt-dlp needs a JS engine to handle some videos. Install one of:
  - [Deno](https://deno.land/)
  - [Node.js](https://nodejs.org/)
  - [Bun](https://bun.sh/)

Python dependencies install automatically via pip. You'll need to install FFmpeg and a JS runtime separately.

> [!TIP]
> **One-click installer coming soon!** A standalone installer that bundles all dependencies is in development.

---

## Platform Support

ViDownloader is primarily tested and supported on:

- **Windows** (10, 11)

Linux support is experimental and has not been fully verified yet.

---

## Building Executables

Want to build a standalone executable? Use the provided `Makefile`:

```bash
make build
```

This works on Windows and will build a single-file executable using **PyInstaller** with all icons bundled into the binary.

Other useful Makefile targets:

```bash
make format   # Auto-format code with black & isort
make lint     # Run flake8, black, and isort checks
make test     # Run the test suite with pytest
make clean    # Remove build artifacts and caches
```

Pre-built executables are available on the [Releases](https://github.com/farhaanaliii/vidownloader/releases) page.

---

## Development & Contribution

This is my first major open-source project, so I'm sure there are plenty of areas to improve. If you find bugs, have feature ideas, or want to contribute code:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details. All contributions are welcome, just try to match the existing code style (`black` + `isort`).

### Dev Setup

```bash
git clone https://github.com/farhaanaliii/vidownloader.git
cd vidownloader
pip install -e ".[dev]"
```

This installs all development dependencies including `pytest`, `black`, `isort`, `flake8`, and `pyinstaller`.

---

## Running Tests

The project has a growing pytest suite (137+ tests):

```bash
make test
# or
pytest
```

---

## License

Released under the **[MIT License](https://opensource.org/licenses/MIT)**. Use it, modify it, share it.

---

## Acknowledgment

ViDownloader handles scraping and UI, while **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** handles video downloads under the hood. Big thanks to the yt-dlp team for building a great tool.

---

## Author

Built by **[Farhan Ali](https://github.com/farhaanaliii)**.
- GitHub: [@farhaanaliii](https://github.com/farhaanaliii)
- Email: i.farhanali.dev@gmail.com
