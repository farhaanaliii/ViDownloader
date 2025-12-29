@echo off
REM ViDownloader Build Script for Windows
REM Builds Qt resources and compiles with Nuitka

setlocal enabledelayedexpansion

echo ==========================================
echo  ViDownloader Build Script (Windows)
echo ==========================================
echo.

REM Configuration
set PROJECT_DIR=%~dp0
set PACKAGE_DIR=%PROJECT_DIR%vidownloader
set QRC_FILE=%PACKAGE_DIR%\resources.qrc
set RC_OUTPUT=%PACKAGE_DIR%\ui\resources_rc.py
set MAIN_FILE=%PACKAGE_DIR%\main.py
set OUTPUT_DIR=%PROJECT_DIR%build
set ICON_FILE=%PACKAGE_DIR%\icons\icon.ico
set VENV_DIR=%PROJECT_DIR%venv

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

REM Step 1: Create/Activate Virtual Environment
echo [1/4] Setting up virtual environment...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo       Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        exit /b 1
    )
)
echo       Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

REM Step 2: Install Dependencies from requirements.txt
echo [2/4] Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
echo       Dependencies installed

REM Step 3: Extract metadata from Constants.py
echo [3/4] Extracting project metadata...
for /f "tokens=1-5 delims=|" %%a in ('python -c "import sys; from datetime import datetime; sys.path.insert(0, chr(46)); from vidownloader.core.Constants import App, Author; print(App.NAME + chr(124) + App.VERSION + chr(124) + Author.NAME + chr(124) + Author.GITHUB_URL + chr(124) + str(datetime.now().year))"') do (
    set TOOL_NAME=%%a
    set TOOL_VERSION=%%b
    set ORG_NAME=%%c
    set ORG_URL=%%d
    set CURRENT_YEAR=%%e
)
set TOOL_DESC=%TOOL_NAME% - A modern YouTube video downloader

echo       Name: %TOOL_NAME%
echo       Version: %TOOL_VERSION%
echo       Author: %ORG_NAME%
echo.

REM Step 4: Build Qt Resources
echo [4/4] Building Qt resources...
where pyrcc5 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pyrcc5 not found. Install PyQt5-tools: pip install pyqt5-tools
    exit /b 1
)

pyrcc5 "%QRC_FILE%" -o "%RC_OUTPUT%"
if errorlevel 1 (
    echo [ERROR] Failed to compile Qt resources
    exit /b 1
)
echo       Resources compiled to: %RC_OUTPUT%

REM Set icon option only if file exists
set ICON_OPT=
if exist "%ICON_FILE%" set ICON_OPT=--windows-icon-from-ico="%ICON_FILE%"

REM Build with Nuitka
echo.
echo Building with Nuitka...
echo       This may take several minutes...
echo.

python -m nuitka ^
    --standalone ^
    --onefile ^
    --enable-plugin=pyqt5 ^
    --include-package=vidownloader ^
    --windows-console-mode=disable ^
    %ICON_OPT% ^
    --company-name="%ORG_NAME%" ^
    --product-name="%TOOL_NAME%" ^
    --file-version="%TOOL_VERSION%" ^
    --product-version="%TOOL_VERSION%" ^
    --copyright="Copyright %CURRENT_YEAR% %ORG_NAME%, %ORG_URL%" ^
    --file-description="%TOOL_DESC%" ^
    --output-dir="%OUTPUT_DIR%" ^
    --output-filename=ViDownloader.exe ^
    --assume-yes-for-downloads ^
    "%MAIN_FILE%"

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    exit /b 1
)

echo.
echo ==========================================
echo  Build Complete!
echo  Output: %OUTPUT_DIR%\ViDownloader.exe
echo ==========================================

REM Create release zip
echo.
echo Creating release package...

REM Detect architecture
set ARCH=x64
if "%PROCESSOR_ARCHITECTURE%"=="x86" set ARCH=x86
if "%PROCESSOR_ARCHITECTURE%"=="ARM64" set ARCH=arm64

set RELEASE_ZIP=%OUTPUT_DIR%\ViDownloader-Windows-%ARCH%.zip


REM Check if PowerShell is available for zip creation
powershell -Command "Compress-Archive -Path '%OUTPUT_DIR%\ViDownloader.exe' -DestinationPath '%RELEASE_ZIP%' -Force" 2>nul
if errorlevel 1 (
    echo [WARNING] Could not create zip archive. PowerShell may not be available.
) else (
    echo       Release package: %RELEASE_ZIP%
)

echo.
echo ==========================================
echo  Release Ready!
echo  Executable: %OUTPUT_DIR%\ViDownloader.exe
echo  ZIP Archive: %RELEASE_ZIP%
echo ==========================================

endlocal

