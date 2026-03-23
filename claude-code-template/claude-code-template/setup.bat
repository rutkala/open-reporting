@echo off
REM
REM Claude Code Template -- Quick Setup Script (Windows)
REM
REM Usage:
REM   setup.bat C:\path\to\your-project "My Project Name"
REM   setup.bat .                        "My Project Name"  (current directory)
REM
REM What it does:
REM   1. Copies .claude\ directory and CLAUDE.md to target project
REM   2. Replaces {PROJECT_NAME} with your project name
REM   3. Creates agent-memory directories
REM   4. Adds recommended .gitignore entries
REM

setlocal enabledelayedexpansion

REM Resolve script directory first (before any pushd)
set "SCRIPT_DIR=%~dp0"

set "TARGET=%~1"
set "PROJECT_NAME=%~2"

REM -- Interactive mode when double-clicked (no arguments) --
if "%TARGET%"=="" (
    echo.
    echo   Claude Code Template Setup
    echo   --------------------------------
    echo.
    echo   This script copies the Claude Code template into your project folder.
    echo   Press Ctrl+C at any time to cancel.
    echo.
    set /p "TARGET=  Target project path (e.g. C:\myproject or . for current dir): "
    echo.
)
if "%PROJECT_NAME%"=="" (
    set /p "PROJECT_NAME=  Project name (e.g. My App): "
    echo.
)

REM Apply defaults if user pressed Enter without typing
if "!TARGET!"=="" set "TARGET=."
if "!PROJECT_NAME!"=="" set "PROJECT_NAME=My Project"

REM Resolve target to absolute path
pushd "!TARGET!" 2>nul
if errorlevel 1 (
    echo.
    echo   ERROR: Directory '!TARGET!' does not exist.
    echo   Please create it first, then re-run setup.bat.
    echo.
    pause
    exit /b 1
)
set "TARGET=%CD%"
popd

echo.
echo   Claude Code Template Setup
echo   --------------------------------
echo   Target:  %TARGET%
echo   Project: %PROJECT_NAME%
echo.

REM -- Check for existing .claude --
if exist "%TARGET%\.claude" (
    echo   WARNING: %TARGET%\.claude already exists.
    set /p "confirm=  Overwrite? (y/N) "
    if /i not "!confirm!"=="y" (
        echo   Aborted.
        pause
        exit /b 0
    )
    echo.
)

REM -- Copy files --
echo   [1/5] Copying .claude\ directory...
xcopy /E /I /Y "%SCRIPT_DIR%.claude" "%TARGET%\.claude" >nul
if errorlevel 1 (
    echo   ERROR: Failed to copy .claude directory.
    pause
    exit /b 1
)

echo   [2/5] Copying CLAUDE.md...
copy /Y "%SCRIPT_DIR%CLAUDE.md" "%TARGET%\CLAUDE.md" >nul
if exist "%SCRIPT_DIR%CLAUDE.example.md" (
    copy /Y "%SCRIPT_DIR%CLAUDE.example.md" "%TARGET%\CLAUDE.example.md" >nul
)

REM -- Replace placeholders --
echo   [3/5] Setting project name...
powershell -NoProfile -Command "(Get-Content '%TARGET%\CLAUDE.md' -Raw) -replace '\{PROJECT_NAME\}', '%PROJECT_NAME%' | Set-Content '%TARGET%\CLAUDE.md' -NoNewline"

REM -- Create agent-memory dir --
echo   [4/5] Creating agent-memory directory...
if not exist "%TARGET%\.claude\agent-memory" mkdir "%TARGET%\.claude\agent-memory"

REM -- Add .gitignore entries --
echo   [5/5] Updating .gitignore...
set "GITIGNORE=%TARGET%\.gitignore"

if not exist "%GITIGNORE%" (
    echo # Claude Code runtime files> "%GITIGNORE%"
)

for %%E in (
    ".claude/agent-activity.log"
    ".claude/agent-activity.jsonl"
    ".claude/.agent-timers/"
    ".claude/.session-pushed"
    ".claude/.lead-last-log"
    ".claude/.hook-errors.log"
) do (
    findstr /C:"%%~E" "%GITIGNORE%" >nul 2>&1
    if errorlevel 1 (
        echo %%~E>> "%GITIGNORE%"
    )
)

echo.
echo   Done! Setup complete.
echo.
echo   Next steps:
echo   --------------------------------
echo   1. Open CLAUDE.md and fill in the CUSTOMIZE sections
if exist "%TARGET%\CLAUDE.example.md" (
echo      (see CLAUDE.example.md for a filled-in reference)
)
echo   2. Edit .claude\languages.json -- set your project language(s)
echo   3. Create domain agents:
echo        copy .claude\agents\_template-domain.md .claude\agents\backend.md
echo        copy .claude\agents\_template-domain.md .claude\agents\frontend.md
echo   4. Edit each agent file with your project's scope and patterns
echo   5. Add permissions to .claude\settings.local.json
echo   6. Open the project in VS Code and start Claude Code
echo   7. Test with: /status-check
echo   8. Watch agents live: node .claude\watch-agents-ui.js
echo.

pause
endlocal
