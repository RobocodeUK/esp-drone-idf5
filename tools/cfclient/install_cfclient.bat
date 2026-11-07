@echo off
setlocal EnableExtensions
REM ======================================================================
REM  Installs the pinned ESP-Drone cfclient into C:\esp\cfclient-venv
REM  1. Installs Python 3.11.9 from python.org if it is missing
REM     (just for this Windows user, no admin needed)
REM  2. Creates the cfclient environment with the exact tested versions
REM  3. Adds a "cfclient (ESP-Drone)" shortcut to the desktop
REM  Needs Git for Windows and internet. Safe to run again at any time.
REM ======================================================================
set "VENV=C:\esp\cfclient-venv"
if defined CFCLIENT_VENV set "VENV=%CFCLIENT_VENV%"
set "PYVER=3.11.9"
set "PYURL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
set "PY311=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

echo.
echo [1/4] Checking for Python 3.11 ...
call :findpy
if defined PY goto :havepy
echo       Not found - downloading Python %PYVER% from python.org ...
set "PYINST=%TEMP%\python-%PYVER%-amd64.exe"
curl.exe -L --fail --progress-bar -o "%PYINST%" "%PYURL%" || goto :fail
echo       Installing Python %PYVER% for this user (1-2 minutes) ...
"%PYINST%" /quiet InstallAllUsers=0 Include_launcher=1 InstallLauncherAllUsers=0 PrependPath=0 Include_test=0 || goto :fail
del "%PYINST%" >NUL 2>&1
call :findpy
if not defined PY (
  echo ERROR: Python %PYVER% did not install correctly.
  goto :fail
)
:havepy
echo       Using "%PY%"

echo.
echo [2/4] Checking for Git ...
git --version >NUL 2>&1 || (echo ERROR: Git not found. Install Git for Windows from git-scm.com, then run this again. & goto :fail)
echo       OK

echo.
echo [3/4] Installing cfclient into %VENV% (about 5 minutes) ...
if not exist "%VENV%\Scripts\python.exe" (
  "%PY%" -m venv "%VENV%" || goto :fail
)
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip || goto :fail
"%VENV%\Scripts\python.exe" -m pip install --force-reinstall --no-deps -r "%~dp0requirements-cfclient.txt" || goto :fail
"%VENV%\Scripts\python.exe" -m pip check || goto :fail

echo.
echo [4/4] Creating desktop shortcut ...
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\cfclient (ESP-Drone).lnk'); $s.TargetPath='%VENV%\Scripts\cfclient.exe'; $s.WorkingDirectory='%VENV%'; $s.Save()" >NUL 2>&1

echo.
echo ============================================================
echo  Done. Start cfclient from the "cfclient (ESP-Drone)" desktop
echo  shortcut, or run:  %VENV%\Scripts\cfclient.exe
echo ============================================================
pause
exit /b 0

:findpy
REM Sets PY to a Python 3.11 interpreter, or leaves it empty.
set "PY="
for /f "delims=" %%i in ('py -3.11 -c "import sys; print(sys.executable)" 2^>NUL') do set "PY=%%i"
if not defined PY if exist "%PY311%" set "PY=%PY311%"
exit /b 0

:fail
echo.
echo Installation FAILED - read the message above.
pause
exit /b 1
