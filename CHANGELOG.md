# Changelog

All notable changes to ViDownloader will be documented in this file.

## Version 1.0.0-beta2 (Current - January 2026)

> [!WARNING]
> **BETA:** This version is functional but may have rough edges. Your feedback helps!

### ✨ New Features

- **NEW:** Flexible video organization system
  - Playlists: Group by playlist name or uploader
  - Single videos: Group in dedicated folder or by uploader
  - Configurable organization settings in Settings dialog
- **NEW:** Real-time download progress tracking
- **NEW:** Video duration display (HH:MM:SS format)
- **NEW:** Video file size display after download completion
- **NEW:** Download button state management (prevents duplicate downloads)

### 🔧 Improvements

- **IMPROVED:** Better error handling for video metadata
- **IMPROVED:** Optimized event handling (reduced duplicate lookups)
- **IMPROVED:** Consolidated video data storage in tree items
- **IMPROVED:** Enhanced YouTube parser for metadata extraction

### 🐛 Bug Fixes

- **FIXED:** Video size display error handling
- **FIXED:** Event type checking improvements
- **FIXED:** Various stability improvements

---

## Version 1.0.0-beta (December 2025)

### Initial Beta Features

- **NEW:** YouTube video & shorts scraping from channels
- **NEW:** Single video/short direct downloads
- **NEW:** Playlist scraping
- **NEW:** Multi-threaded bulk downloads (1-10 concurrent threads)
- **NEW:** Pause/Resume download capability
- **NEW:** Export/Import video lists (.viio format)
- **NEW:** Flexible file naming (title, video ID, or random)
- **NEW:** Modern PyQt5 interface with real-time progress tracking
- **NEW:** Configurable download and export directories

### Coming Soon

- **NEW:** Quality selection (720p, 1080p, 4K)
- **NEW:** Advanced filtering and search in video lists
- **NEW:** Download history and statistics
- **IMPROVED:** Better performance and memory optimization
- **IMPROVED:** Enhanced error handling and retry logic
