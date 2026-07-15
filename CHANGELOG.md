# Changelog

All notable changes to ViDownloader will be documented in this file.

## Unreleased

---

## [v0.3.0] - June 2026

### ✨ New Features

- **NEW:** Comprehensive pytest suite with 137 tests
- **NEW:** Proper window navigation with process safety checks
- **NEW:** Uploader fallback for playlist video metadata extraction
- **NEW:** Fallback path for playlist name extraction
- **NEW:** Separate release notes dialog with toolbar buttons

### 🔧 Improvements

- **IMPROVED:** Switched build toolchain from Nuitka to PyInstaller
- **IMPROVED:** Replaced shell scripts with Makefile for cross-platform builds
- **IMPROVED:** Unified CI/CD with multi-platform matrix build workflow
- **IMPROVED:** Applied black & isort code formatting across entire codebase
- **IMPROVED:** Tree widget: removed select column, using custom data role
- **IMPROVED:** Improved tree widget column sizing and user interaction
- **IMPROVED:** Unified filename restrictions across all platforms
- **IMPROVED:** Added StrEnum fallback for Python 3.10 compatibility
- **IMPROVED:** Cross-platform support documentation in README

### 🐛 Bug Fixes

- **FIXED:** YouTube API response parsing for updated video metadata structure
- **FIXED:** Makefile clean target for cross-platform (Windows) support

---

## [v0.2.0] - January 2026

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

## [v0.1.0] - December 2025

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
