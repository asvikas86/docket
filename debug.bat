@echo off
REM Runs the already-built Docket.exe with DevTools enabled, so you can
REM right-click inside the app and choose "Inspect" to see console errors.
REM Normal double-clicking of Docket.exe does NOT show DevTools - this
REM script is only for troubleshooting.

cd /d "%~dp0"

if not exist "dist\Docket.exe" (
    echo dist\Docket.exe not found - build it first by running build.bat.
    pause
    exit /b 1
)

set DOCKET_DEBUG=1
start "" "dist\Docket.exe"
