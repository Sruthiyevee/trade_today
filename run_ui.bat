@echo off
echo =========================================================
echo Starting Multi-Factor Trading Analyst UI (Streamlit)
echo =========================================================

REM Move to the workspace root directory
cd /d "%~dp0"

echo [INFO] Activating Master Virtual Environment...
call .venv\Scripts\activate.bat

echo [INFO] Setting PYTHONPATH to ensure seamless directory importing...
set PYTHONPATH=%cd%

echo [INFO] Launching Streamlit UI on localhost:8501...
cd Phase_6_Web_UI
streamlit run frontend\streamlit_app.py

pause
