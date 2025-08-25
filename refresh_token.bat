@echo off
REM Token Refresh Batch Script
REM This script runs the Python token refresh script

echo Starting token refresh...
cd /d "d:\Projects\back up\FoodVault"

REM Set environment variable to indicate automated run
set AUTOMATED_RUN=1

REM Run the Python script
"C:/Program Files/Python310/python.exe" refresh_token.py

REM Log the result
if %ERRORLEVEL% == 0 (
    echo Token refresh completed successfully at %date% %time% >> token_refresh.log
) else (
    echo Token refresh failed at %date% %time% >> token_refresh.log
)

echo Token refresh completed.
