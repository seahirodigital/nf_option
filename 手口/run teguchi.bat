@echo off
cd /d "%~dp0app"
echo Starting Teguchi App...
start http://127.0.0.1:8000/
python teguchi.py
pause
