@echo off
echo Starting Teybr oS...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo Application crashed with error code %errorlevel%.
)
pause
