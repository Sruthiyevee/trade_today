@echo off
echo =========================================================
echo Starting Multi-Factor Trading Analyst UI (Streamlit)
echo =========================================================

REM Move into Phase 6 Directory
cd /d "%~dp0Phase_6_Web_UI"

REM Check if the venv exists, if not, create and install
IF NOT EXIST ".venv" (
    echo [INFO] Creating Python Virtual Environment for Phase 6...
    python -m venv .venv
    echo [INFO] Installing required dependencies...
    call .\.venv\Scripts\activate.bat
    pip install -r requirements.txt
) ELSE (
    echo [INFO] Virtual Environment found. Activating...
    call .\.venv\Scripts\activate.bat
)

echo [INFO] Launching Streamlit UI on localhost:8501...
streamlit run frontend\streamlit_app.py

pause
