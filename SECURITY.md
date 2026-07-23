# Security Policy

## Supported Versions

Only the latest release receives security fixes.

| Version | Supported |
|---------|-----------|
| Latest  | ✅        |
| Older   | ❌        |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, report it privately by emailing:

**📧 i.farhanali.de@gmail.com**

Include as much detail as possible:

- A description of the vulnerability
- Steps to reproduce the issue
- The potential impact
- Any suggested fixes (optional)

You can expect a response within **72 hours**. Once the issue is confirmed, a fix will be released as soon as possible and you'll be credited (unless you prefer to remain anonymous).

## Scope

This project:
- Scrapes YouTube metadata via their internal API
- Downloads videos using **yt-dlp**
- Stores user settings locally (no cloud sync, no remote telemetry)

Relevant areas to consider:
- Malicious `.viio` import files
- Unsafe URL handling
- Dependency vulnerabilities (yt-dlp, PySide6, curl_cffi)
