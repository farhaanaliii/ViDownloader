#!/bin/bash
# ViDownloader Build Script for Linux/macOS
# Builds Qt resources and compiles with Nuitka

set -e

echo "=========================================="
echo " ViDownloader Build Script (Linux/macOS)"
echo "=========================================="
echo ""

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/vidownloader"
QRC_FILE="$PACKAGE_DIR/resources.qrc"
RC_OUTPUT="$PACKAGE_DIR/ui/resources_rc.py"
MAIN_FILE="$PACKAGE_DIR/main.py"
OUTPUT_DIR="$SCRIPT_DIR/build"
ICON_FILE="$PACKAGE_DIR/icons/icon.png"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed or not in PATH"
    exit 1
fi

# Extract metadata from Constants.py using single Python call
echo "[0/4] Extracting project metadata..."
IFS='|' read -r TOOL_NAME TOOL_VERSION ORG_NAME ORG_URL CURRENT_YEAR <<< $(python3 -c "import sys; from datetime import datetime; sys.path.insert(0, '.'); from vidownloader.core.Constants import App, Author; print(f'{App.NAME}|{App.VERSION}|{Author.NAME}|{Author.ORG_URL}|{datetime.now().year}')")
TOOL_DESC="$TOOL_NAME - A modern YouTube video downloader"

echo "      Name: $TOOL_NAME"
echo "      Version: $TOOL_VERSION"
echo "      Author: $ORG_NAME"
echo ""

# Step 1: Build Qt Resources
echo "[1/4] Building Qt resources..."
if ! command -v pyrcc5 &> /dev/null; then
    echo "[ERROR] pyrcc5 not found. Install PyQt5-tools: pip install pyqt5-tools"
    exit 1
fi

pyrcc5 "$QRC_FILE" -o "$RC_OUTPUT"
echo "      Resources compiled to: $RC_OUTPUT"

# Step 2: Check/Install Nuitka
echo "[2/4] Checking Nuitka..."
if ! python3 -c "import nuitka" &> /dev/null; then
    echo "      Nuitka not found, installing..."
    pip3 install nuitka
fi

# Step 3: Check icon exists
echo "[3/4] Preparing icon..."
if [ ! -f "$ICON_FILE" ]; then
    echo "[WARNING] Icon file not found at $ICON_FILE"
fi

# Step 4: Build with Nuitka
echo "[4/4] Building with Nuitka..."
echo "      This may take several minutes..."
echo ""

# Build command - Linux/macOS metadata options
# Note: Windows-specific metadata (company-name, product-name, etc.) are applied
# only when building on Windows. On Linux, we use --linux-icon for desktop integration.
python3 -m nuitka \
    --standalone \
    --enable-plugin=pyqt5 \
    --include-package=vidownloader \
    --linux-icon="$ICON_FILE" \
    --output-dir="$OUTPUT_DIR" \
    --output-filename="$TOOL_NAME" \
    --assume-yes-for-downloads \
    "$MAIN_FILE"

echo ""
echo "=========================================="
echo " Build Complete!"
echo " Output: $OUTPUT_DIR/main.dist/"
echo "=========================================="

# Create release package
echo ""
echo "Creating release package..."

# Determine platform for naming
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
else
    PLATFORM="Linux"
fi

# Detect architecture
MACHINE_ARCH=$(uname -m)
case "$MACHINE_ARCH" in
    x86_64)  ARCH="x64" ;;
    aarch64) ARCH="arm64" ;;
    arm64)   ARCH="arm64" ;;
    i686)    ARCH="x86" ;;
    *)       ARCH="$MACHINE_ARCH" ;;
esac

RELEASE_NAME="ViDownloader-${PLATFORM}-${ARCH}"
RELEASE_DIR="$OUTPUT_DIR/$RELEASE_NAME"
RELEASE_ZIP="$OUTPUT_DIR/${RELEASE_NAME}.zip"
RELEASE_TAR="$OUTPUT_DIR/${RELEASE_NAME}.tar.gz"

# Copy build to release directory
rm -rf "$RELEASE_DIR"
cp -r "$OUTPUT_DIR/main.dist" "$RELEASE_DIR"

# Create zip archive
if command -v zip &> /dev/null; then
    cd "$OUTPUT_DIR"
    zip -r "$RELEASE_NAME.zip" "$RELEASE_NAME"
    echo "      ZIP created: $RELEASE_ZIP"
fi

# Create tar.gz archive
cd "$OUTPUT_DIR"
tar -czf "${RELEASE_NAME}.tar.gz" "$RELEASE_NAME"
echo "      TAR.GZ created: $RELEASE_TAR"

echo ""
echo "=========================================="
echo " Release Ready!"
echo " Directory: $RELEASE_DIR"
echo " Archives:  $RELEASE_ZIP"
echo "            $RELEASE_TAR"
echo "=========================================="

