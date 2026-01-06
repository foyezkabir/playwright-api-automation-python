@echo off
REM Run tests and automatically update README with results
echo ========================================
echo Running Tests and Updating README
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the update script
python sync_readme_test_results.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ Success! README updated with latest test results
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ❌ Failed to update README
    echo ========================================
)

pause
