@echo off
REM Installs the pinned ESP-Drone cfclient into C:\esp\cfclient-venv
REM Needs Python 3.11 installed (python.org). Python 3.13 will NOT work.
setlocal
set VENV=C:\esp\cfclient-venv
py -3.11 --version >NUL 2>&1 || (echo Python 3.11 not found. Install it from python.org first. & exit /b 1)
if not exist "%VENV%\Scripts\python.exe" py -3.11 -m venv "%VENV%" || exit /b 1
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip || exit /b 1
"%VENV%\Scripts\python.exe" -m pip install --no-deps -r "%~dp0requirements-cfclient.txt" || exit /b 1
"%VENV%\Scripts\python.exe" -m pip check || exit /b 1
echo.
echo Done. Start cfclient with:  %VENV%\Scripts\cfclient.exe
