@echo off
echo Starting Million Journey Server...
echo Please ensure that this command prompt stays open while you play.
start http://localhost:8000
python -m http.server 8000
pause
