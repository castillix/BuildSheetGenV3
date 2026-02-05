@echo off
echo ================================================
echo Build Sheet Generator V3 - Starting Server
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Start the Flask server
echo.
echo Starting web server...
echo Access the application at: http://localhost:5000
echo Or from another computer: http://YOUR-IP-ADDRESS:5000
echo.
echo Press CTRL+C to stop the server
echo.
python app.py

pause
