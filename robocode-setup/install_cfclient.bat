@echo off
setlocal EnableExtensions
REM ======================================================================
REM  Installs the pinned ESP-Drone cfclient into C:\esp\cfclient-venv
REM  (SETUP.bat runs this for you; you can also run it on its own.)
REM  1. Installs Python 3.11.9 from python.org if it is missing
REM     (just for this Windows user, no admin needed)
REM  2. Creates the cfclient environment with the exact tested versions
REM  3. Adds a "cfclient (ESP-Drone)" shortcut to the desktop
REM  Needs Git and internet. Safe to run again at any time.
REM ======================================================================
set "HERE=%~dp0"
set "DL=%HERE%downloads"
set "VENV=C:\esp\cfclient-venv"
if defined CFCLIENT_VENV set "VENV=%CFCLIENT_VENV%"
set "PYURL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
set "PYSHA=5ee42c4eee1e6b4464bb23722f90b45303f79442df63083f05322f1785f5fdde"
set "PY311=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

echo.
echo [cfclient 1/4] Checking for Python 3.11 ...
call :findpy
if defined PY goto :havepy
echo       Not found - installing Python 3.11.9 for this user.
powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%download_and_verify.ps1" -Url "%PYURL%" -Out "%DL%\python-3.11.9-amd64.exe" -Sha256 %PYSHA% || goto :fail
echo       Installing (1-2 minutes) ...
"%DL%\python-3.11.9-amd64.exe" /quiet InstallAllUsers=0 Include_launcher=1 InstallLauncherAllUsers=0 PrependPath=0 Include_test=0 || goto :fail
call :findpy
if not defined PY (
  echo ERROR: Python 3.11.9 did not install correctly.
  goto :fail
)
:havepy
echo       Using "%PY%"

echo.
echo [cfclient 2/4] Checking for Git ...
git --version >NUL 2>&1 || (echo ERROR: Git not found. Run SETUP.bat, or install Git from DOWNLOAD_LINKS.txt. & goto :fail)
echo       OK

echo.
echo [cfclient 3/4] Installing cfclient into %VENV% (about 5 minutes) ...
if not exist "%VENV%\Scripts\python.exe" (
  "%PY%" -m venv "%VENV%" || goto :fail
)
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip || goto :fail
"%VENV%\Scripts\python.exe" -m pip install --force-reinstall --no-deps -r "%HERE%requirements-cfclient.txt" || goto :fail
"%VENV%\Scripts\python.exe" -m pip check || goto :fail

echo.
echo [cfclient 4/4] Creating desktop shortcut ...
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\cfclient (ESP-Drone).lnk'); $s.TargetPath='%VENV%\Scripts\cfclient.exe'; $s.WorkingDirectory='%VENV%'; $s.Save()" >NUL 2>&1

echo.
echo       cfclient installed. Desktop shortcut: "cfclient (ESP-Drone)"
if not defined NOPAUSE pause
exit /b 0

:findpy
REM Sets PY to a Python 3.11 interpreter, or leaves it empty.
set "PY="
for /f "delims=" %%i in ('py -3.11 -c "import sys; print(sys.executable)" 2^>NUL') do set "PY=%%i"
if not defined PY if exist "%PY311%" set "PY=%PY311%"
exit /b 0

:fail
echo.
echo cfclient installation FAILED - read the message above.
if not defined NOPAUSE pause
exit /b 1
