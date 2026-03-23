@echo off
title Agent Activity Monitor (Web)
echo.
echo   Starting Agent Activity Monitor...
echo.
node "%~dp0watch-agents-ui.js"
pause
