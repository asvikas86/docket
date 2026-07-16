@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo  Docket - build script
echo ============================================
echo.
echo Step 1/2: Installing dependencies...
echo.

py -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [FAILED] Could not install dependencies.
    echo Make sure Python is installed from https://python.org
    echo ^(with "Add python.exe to PATH" checked^), then try again.
    echo See README.md for more troubleshooting.
    pause
    exit /b 1
)

echo.
echo Step 2/2: Building Docket.exe ...
echo.

py -m PyInstaller --onefile --windowed --name Docket --icon assets\icon.ico --add-data "index.html;." app.py
if errorlevel 1 (
    echo.
    echo [FAILED] Build did not complete. See the messages above,
    echo or the Troubleshooting section in README.md.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Done!
echo ============================================
echo.
echo Your app is ready at:  dist\Docket.exe
echo.
echo To get a clickable icon like a normal Windows app:
echo   1. Open the "dist" folder that just appeared.
echo   2. Right-click Docket.exe.
echo   3. Choose "Show more options" then "Send to" then
echo      "Desktop (create shortcut)".
echo   4. (Optional) Right-click the new desktop shortcut and choose
echo      "Pin to Start" or "Pin to taskbar".
echo.
echo That shortcut opens Docket directly - no Python, no terminal,
echo no typing a command every time.
echo.
pause
