@echo off
setlocal EnableExtensions
title Robocode ESP-Drone setup
REM ======================================================================
REM  Robocode ESP-Drone - one-click setup for a Windows PC
REM   1. Git for Windows 2.47.1
REM   2. ESP-IDF 5.0.7 (build tools for the drone firmware)
REM   3. Python 3.11.9 + cfclient (PC app for the drone)
REM  Anything already installed is skipped. Every installer is downloaded
REM  from a pinned official link (see DOWNLOAD_LINKS.txt) and checked
REM  against its SHA-256 fingerprint before it is run.
REM ======================================================================
set "HERE=%~dp0"
set "DL=%HERE%downloads"
set "GITURL=https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe"
set "GITSHA=25527923debc06515b3016f2d6bca0820656e8281a23be2f43bfb658bd5dda70"
set "IDFURL=https://dl.espressif.com/dl/idf-installer/esp-idf-tools-setup-offline-5.0.7.exe"
set "IDFSHA=25068a62f0ac840e5f058a36d013864d3c27751a2344f62f3a14bb3288c8eedc"
set "IDFDIR=C:\Espressif\frameworks\esp-idf-v5.0.7"

echo ==================================================================
echo   Robocode ESP-Drone setup
echo ==================================================================
echo   This installs everything needed to flash and fly the ESP-Drone.
echo   - It may download up to about 1 GB. Keep the PC plugged in.
echo   - Windows may ask "Do you want to allow this app to make
echo     changes?" - click Yes.
echo   - Takes 20-40 minutes on a new PC. Do not close this window.
echo.
if /i not "%HERE%"=="C:\esp\esp-drone-idf5\robocode-setup\" (
  echo   NOTE: this folder is %HERE%
  echo         The guide expects the code at C:\esp\esp-drone-idf5. Long paths
  echo         or paths with spaces can break the firmware build.
  echo.
)
if not defined NOPAUSE pause

REM ---------------------------------------------------------------- Git
echo.
echo [1/3] Git for Windows
call :findgit
if defined HAVEGIT (
  echo       Already installed.
  goto :idf
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%download_and_verify.ps1" -Url "%GITURL%" -Out "%DL%\Git-2.47.1-64-bit.exe" -Sha256 %GITSHA% || goto :fail
echo       Installing Git (1-2 minutes). Click Yes if Windows asks for permission.
start "" /wait "%DL%\Git-2.47.1-64-bit.exe" /VERYSILENT /NORESTART /NOCANCEL /SP- /SUPPRESSMSGBOXES
call :findgit
if not defined HAVEGIT (
  echo ERROR: Git did not install. Run SETUP.bat again and click Yes on the permission prompt.
  goto :fail
)
echo       Git installed.

REM ---------------------------------------------------------------- ESP-IDF
:idf
echo.
echo [2/3] ESP-IDF 5.0.7
if exist "%IDFDIR%\export.bat" (
  echo       Already installed in %IDFDIR%
  goto :cfclient
)
echo       This download is about 916 MB.
powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%download_and_verify.ps1" -Url "%IDFURL%" -Out "%DL%\esp-idf-tools-setup-offline-5.0.7.exe" -Sha256 %IDFSHA% || goto :fail
echo.
echo       The ESP-IDF installer window will open now:
echo        - Click Yes if Windows asks for permission.
echo        - Keep all the default choices (folder C:\Espressif, drivers ticked).
echo        - If it offers to apply fixes such as long path support, accept.
echo        - Click Install, wait 15-30 minutes, then click Finish.
echo       This window carries on when the installer closes.
start "" /wait "%DL%\esp-idf-tools-setup-offline-5.0.7.exe"
if not exist "%IDFDIR%\export.bat" (
  echo ERROR: ESP-IDF 5.0.7 was not found in %IDFDIR% after the installer closed.
  echo        Run SETUP.bat again and keep the default install folder.
  goto :fail
)
echo       ESP-IDF installed.

REM ---------------------------------------------------------------- cfclient
:cfclient
echo.
echo [3/3] Python 3.11 and cfclient
set "NOPAUSE_SAVED=%NOPAUSE%"
set "NOPAUSE=1"
call "%HERE%install_cfclient.bat" || goto :fail
set "NOPAUSE=%NOPAUSE_SAVED%"

echo.
echo ==================================================================
echo   Setup complete.
echo ==================================================================
echo   Next: flash the drone (guide Part C) using the "ESP-IDF 5.0 CMD"
echo   shortcut in the Start menu, then open "cfclient (ESP-Drone)" from
echo   the desktop. The guide is ROBOCODE_SETUP_GUIDE.pdf in this folder.
echo.
echo   You can delete the "downloads" folder here to free about 1 GB.
echo.
if not defined NOPAUSE pause
exit /b 0

:findgit
REM Sets HAVEGIT=1 if git works, adding the default Git folder to PATH if needed.
set "HAVEGIT="
git --version >NUL 2>&1 && set "HAVEGIT=1"
if defined HAVEGIT exit /b 0
if exist "%ProgramFiles%\Git\cmd\git.exe" (
  set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
  set "HAVEGIT=1"
)
exit /b 0

:fail
echo.
echo ==================================================================
echo   Setup FAILED - read the message above, fix it, then run
echo   SETUP.bat again. Finished steps are skipped next time.
echo ==================================================================
if not defined NOPAUSE pause
exit /b 1
