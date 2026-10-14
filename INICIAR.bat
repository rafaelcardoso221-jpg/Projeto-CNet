@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if exist "BaseBot.exe" (
    "BaseBot.exe"
) else (
    if exist ".venv\Scripts\python.exe" (
        ".venv\Scripts\python.exe" "basebot.py"
    ) else (
        py -3 "basebot.py"
    )
)
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" (
    echo.
    echo Rotina interrompida ou com erro. Consulte a pasta logs.
    echo Se der erro, envie o arquivo de log, nunca o webhook.
    echo Sem BaseBot.exe? Instale Python/dependencias conforme README.md.
    pause
)
exit /b %RESULT%
