@echo off
title Agent Activity Monitor (Terminal)
powershell -NoExit -Command "Get-Content '%~dp0agent-activity.log' -Wait"
