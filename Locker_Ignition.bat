@echo off
title SENTIENT SYNC // MISSION CONTROL
echo [!] INITIALIZING DEFENSE GRID...
start cmd /k "python api.py"
timeout /t 2
start cmd /k "python sentinel.py"
timeout /t 2
cd frontend/frontend
start cmd /k "npm run dev"
echo [!] ALL SYSTEMS NOMINAL. SECURE THE AGI.
pause
