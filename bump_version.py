"""
Version Bump Script for ViDownloader
Updates version in both pyproject.toml and Constants.py

Usage:
    python bump_version.py 1.2.0
    python bump_version.py --show  # Show current version
"""

import sys
import re
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PYPROJECT_FILE = PROJECT_DIR / "pyproject.toml"
CONSTANTS_FILE = PROJECT_DIR / "vidownloader" / "core" / "Constants.py"


def get_current_version() -> str:
    """Read current version from Constants.py"""
    content = CONSTANTS_FILE.read_text(encoding="utf-8")
    match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else "unknown"


def validate_version(version: str) -> bool:
    """Validate semantic version format (X.Y.Z)"""
    return bool(re.match(r'^\d+\.\d+\.\d+$', version))


def update_constants(new_version: str) -> bool:
    """Update version in Constants.py"""
    content = CONSTANTS_FILE.read_text(encoding="utf-8")
    updated = re.sub(
        r'(VERSION\s*=\s*["\'])[^"\']+(["\'])',
        rf'\g<1>{new_version}\g<2>',
        content
    )
    CONSTANTS_FILE.write_text(updated, encoding="utf-8")
    return True


def update_pyproject(new_version: str) -> bool:
    """Update version in pyproject.toml"""
    content = PYPROJECT_FILE.read_text(encoding="utf-8")
    updated = re.sub(
        r'(version\s*=\s*["\'])[^"\']+(["\'])',
        rf'\g<1>{new_version}\g<2>',
        content
    )
    PYPROJECT_FILE.write_text(updated, encoding="utf-8")
    return True


def main():
    if len(sys.argv) < 2:
        print(f"Current version: {get_current_version()}")
        print("\nUsage: python bump_version.py <new_version>")
        print("Example: python bump_version.py 1.2.0")
        sys.exit(0)

    if sys.argv[1] == "--show":
        print(get_current_version())
        sys.exit(0)

    new_version = sys.argv[1]
    
    if not validate_version(new_version):
        print(f"[ERROR] Invalid version format: {new_version}")
        print("Version must be in format X.Y.Z (e.g., 1.2.0)")
        sys.exit(1)

    current = get_current_version()
    print(f"Bumping version: {current} -> {new_version}")
    
    update_constants(new_version)
    print(f"  ✓ Updated Constants.py")
    
    update_pyproject(new_version)
    print(f"  ✓ Updated pyproject.toml")
    
    print(f"\nVersion bumped to {new_version}")


if __name__ == "__main__":
    main()
