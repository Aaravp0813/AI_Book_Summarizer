@echo off
title AI Book Summarizer Launcher
mode con: cols=70 lines=22
color 0B

:START_SERVERS
cls
echo =====================================================================
echo     __  __    _   _    _   _    ____   _   _  _____ ____  
echo    ^|  \/  ^|  ^| ^| ^| ^|  ^| \ ^| ^|  / ___^| ^| ^| ^| ^|^| ____^|  _ \ 
echo    ^| ^|\/^| ^|  ^| ^| ^| ^|  ^|  \^| ^| ^| ^|    ^| ^|_^| ^|^|  _^|  ^| ^|_) ^|
echo    ^| ^|  ^| ^|  ^| ^|_^| ^|  ^| ^|\  ^| ^| ^|___ ^|  _  ^|^| ^|___ ^|  _ ^_ ^_ 
echo    ^|_^|  ^|_^|   \___/   ^|_^| \_^|  \____^| ^|_^| ^|_^|^|_____^|_^| \_\
echo.                                                    
echo =====================================================================
echo  [CLEANUP] Ensuring old server processes are closed...
taskkill /f /im node.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
timeout /t 1 >nul

echo  [+] Launching Vite Frontend...
start "⚡ React Frontend Server" cmd /k "color 0E && title Vite Development Server && cd /d E:\My_Projects\AI_Book_Summarizer\frontend && npm run dev"

echo  [+] Launching FastAPI Backend...
start "🐍 FastAPI Backend Server" cmd /k "color 0A && title FastAPI Uvicorn Server && cd /d E:\My_Projects\AI_Book_Summarizer\backend && python -m uvicorn main:app --reload"

echo.
echo ---------------------------------------------------------------------
echo  [WAITING] FastAPI is loading FAISS Databases...
echo  (This will unlock automatically once "Startup Complete" is reached)
echo ---------------------------------------------------------------------
<nul set /p "=Loading: "

:PING_LOOP
timeout /t 2 >nul
<nul set /p "=. "

:: Use Windows 'netstat' to check if the port is actively listening/responding instead of curl HTTP codes
netstat -ano | findstr 127.0.0.1:8000 | findstr LISTENING >nul 2>&1

if %errorlevel% neq 0 (
    goto PING_LOOP
)

:: Give it exactly 5 more seconds to finish loading those heavy embedding models after the port opens
timeout /t 5 >nul

:MENU
cls
echo =====================================================================
echo                AI BOOK SUMMARIZER CONTROL PANEL                      
echo =====================================================================
echo.
echo    STATUS       :  [92mONLINE / ACTIVE [0m
echo.
echo    LOCAL APPLICATION URLS (Ctrl+Click to Open):
echo    -----------------------------------------------------------------
echo     [93mFRONTEND URL :  http://localhost:5173 [0m
echo     [92mBACKEND API  :  http://127.0.0.1:8000 [0m
echo     [96mDOCS (SWAGGER): http://127.0.0 [0m
echo    -----------------------------------------------------------------
echo.
echo    SHUTDOWN OPTIONS:
echo   =========================================
echo    [1] Turn Off (Close everything)
echo    [2] Turn Off (Close everything)
echo    [turn off] Type words to close everything
echo   =========================================
echo.

set /p user_choice="Enter choice or command: "

if "%user_choice%"=="1" goto SHUTDOWN
if "%user_choice%"=="2" goto SHUTDOWN
if /i "%user_choice%"=="turn off" goto SHUTDOWN

echo Invalid option. Keeping servers running...
timeout /t 2 >nul
goto MENU

:SHUTDOWN
cls
echo =====================================================================
echo  [SHUTDOWN] Terminating development servers safely...
echo =====================================================================
echo.

taskkill /f /im node.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1

echo  [SUCCESS] Frontend and Backend processes have been stopped.
timeout /t 3 >nul
exit
