#!/bin/bash

# ==========================================
#  ViDownloader Build Script (Linux)
# ==========================================

set -e  # Exit on error

echo
echo "=========================================="
echo " ViDownloader Build Script (Linux)"
echo "=========================================="
echo

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$PROJECT_DIR/vidownloader"
QRC_FILE="$PACKAGE_DIR/resources.qrc"
RC_OUTPUT="$PACKAGE_DIR/ui/resources_rc.py"
MAIN_FILE="$PACKAGE_DIR/main.py"
OUTPUT_DIR="$PROJECT_DIR/build"
ICON_FILE="$PACKAGE_DIR/icons/icon.png"
VENV_DIR="$PROJECT_DIR/venv"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed or not in PATH"
    exit 1
fi

# Step 1: Create/Activate Virtual Environment
echo "[1/4] Setting up virtual environment..."
if [ ! -d "$VENV_DIR/bin" ]; then
    echo "       Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
fi
echo "       Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Step 2: Install Dependencies from requirements.txt
echo "[2/4] Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "       Dependencies installed"

# Step 3: Extract metadata from Constants.py
echo "[3/4] Extracting project metadata..."
cd "$PROJECT_DIR"

# Using Python to extract metadata
read -r TOOL_NAME TOOL_VERSION ORG_NAME ORG_URL CURRENT_YEAR <<< $(python3 -c "
import sys
from datetime import datetime
sys.path.insert(0, '.')
try:
    from vidownloader.core.Constants import App, Author
    print(f'{App.NAME}|{App.VERSION}|{Author.NAME}|{Author.GITHUB_URL}|{datetime.now().year}')
except ImportError as e:
    print(f'Error: {e}')
    sys.exit(1)
")

if [[ "$TOOL_NAME" == Error:* ]]; then
    echo "[ERROR] Failed to import Constants module: $TOOL_NAME"
    exit 1
fi

TOOL_DESC="$TOOL_NAME - A modern YouTube video downloader"

# Extract numeric version (e.g., 1.0.0-beta -> 1.0.0)
FILE_VERSION="${TOOL_VERSION%%-*}"

echo "       Name: $TOOL_NAME"
echo "       Version: $TOOL_VERSION (File Version: $FILE_VERSION)"
echo "       Author: $ORG_NAME"
echo

# Step 4: Build Qt Resources
echo "[4/4] Building Qt resources..."
if ! command -v pyrcc5 &> /dev/null; then
    # Try to find pyrcc5 in virtual environment
    if [ -f "$VENV_DIR/bin/pyrcc5" ]; then
        PYTHONPATH="$VENV_DIR/bin:$PYTHONPATH"
    else
        echo "[ERROR] pyrcc5 not found. Install PyQt5-tools: pip install pyqt5-tools"
        exit 1
    fi
fi

pyrcc5 "$QRC_FILE" -o "$RC_OUTPUT"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to compile Qt resources"
    exit 1
fi
echo "       Resources compiled to: $RC_OUTPUT"

# Build with Nuitka
echo
echo "Building with Nuitka..."
echo "       This may take several minutes..."
echo

# Detect architecture
ARCH=$(uname -m)
case $ARCH in
    x86_64)
        ARCH="x64"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        ;;
    arm*)
        ARCH="arm"
        ;;
    i386|i686)
        ARCH="x86"
        ;;
    *)
        ARCH="unknown"
        ;;
esac

# Prepare Nuitka arguments
NUITKA_ARGS=(
    --standalone
    --onefile
    --enable-plugin=pyqt5
    --include-package=vidownloader
    --output-dir="$OUTPUT_DIR"
    --output-filename=ViDownloader
    --assume-yes-for-downloads
)

# Add icon if exists (for Linux desktop entry)
if [ -f "$ICON_FILE" ]; then
    NUITKA_ARGS+=(--linux-icon="$ICON_FILE")
fi

# Add metadata
NUITKA_ARGS+=(
    --company-name="$ORG_NAME"
    --product-name="$TOOL_NAME"
    --file-version="$FILE_VERSION"
    --product-version="$FILE_VERSION"
    --copyright="Copyright $CURRENT_YEAR $ORG_NAME, $ORG_URL"
    --file-description="$TOOL_DESC"
)

python3 -m nuitka "${NUITKA_ARGS[@]}" "$MAIN_FILE"

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Build failed!"
    exit 1
fi

echo
echo "=========================================="
echo " Build Complete!"
echo " Output: $OUTPUT_DIR/ViDownloader"
echo "=========================================="

# Create release tarball
echo
echo "Creating release package..."

RELEASE_TAR="$OUTPUT_DIR/ViDownloader-Linux-$ARCH.tar.gz"
RELEASE_DIR="$OUTPUT_DIR/ViDownloader-Linux-$ARCH"

# Create directory structure for distribution
mkdir -p "$RELEASE_DIR"
cp "$OUTPUT_DIR/ViDownloader" "$RELEASE_DIR/"
if [ -f "$ICON_FILE" ]; then
    mkdir -p "$RELEASE_DIR/icons"
    cp "$ICON_FILE" "$RELEASE_DIR/icons/"
fi

# Create a simple README
cat > "$RELEASE_DIR/README.txt" << EOF
ViDownloader - Linux Version
============================

Version: $TOOL_VERSION
Architecture: $ARCH
Build Date: $(date)

Installation:
1. Extract this archive: tar -xzf $(basename "$RELEASE_TAR")
2. Run the executable: ./ViDownloader

Dependencies (if not bundled):
- libgl1-mesa-glx
- libxcb-xinerama0

Note: The executable is built with Nuitka and should be self-contained.
EOF

# Create desktop entry
if [ -f "$ICON_FILE" ]; then
    cat > "$RELEASE_DIR/ViDownloader.desktop" << EOF
[Desktop Entry]
Type=Application
Name=$TOOL_NAME
Comment=$TOOL_DESC
Exec=./ViDownloader
Icon=./icons/$(basename "$ICON_FILE")
Categories=AudioVideo;Network;
Terminal=false
EOF
fi

# Create tarball
tar -czf "$RELEASE_TAR" -C "$OUTPUT_DIR" "ViDownloader-Linux-$ARCH"

echo "       Release package: $RELEASE_TAR"
echo

echo "=========================================="
echo " Release Ready!"
echo " Executable: $OUTPUT_DIR/ViDownloader"
echo " Tarball: $RELEASE_TAR"
echo "=========================================="

# Make executable executable
chmod +x "$OUTPUT_DIR/ViDownloader"

echo
echo "To run the application:"
echo "  $OUTPUT_DIR/ViDownloader"
echo
echo "To install system-wide (optional):"
echo "  sudo cp $OUTPUT_DIR/ViDownloader /usr/local/bin/"
echo