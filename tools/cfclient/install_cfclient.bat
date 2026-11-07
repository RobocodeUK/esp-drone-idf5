@echo off
REM Installs the pinned ESP-Drone cfclient into C:\esp\cfclient-venv
REM Needs Python 3.11 (python.org) and Git for Windows. Python 3.13 will NOT work.
REM Safe to run again: it reinstalls the exact pinned versions.
setlocal
set VENV=C:\esp\cfclient-venv

py -3.11 --version >NUL 2>&1 || (echo ERROR: Python 3.11 not found. Install Python 3.11.9 from python.org first. & goto :fail)
git --version >NUL 2>&1 || (echo ERROR: Git not found. Install Git for Windows from git-scm.com first. & goto :fail)

if not exist "%VENV%\Scripts\python.exe" (
  echo Creating %VENV% ...
  py -3.11 -m venv "%VENV%" || goto :fail
)
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip || goto :fail
"%VENV%\Scripts\python.exe" -m pip install --force-reinstall --no-deps -r "%~dp0requirements-cfclient.txt" || goto :fail
"%VENV%\Scripts\python.exe" -m pip check || goto :fail

powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\cfclient (ESP-Drone).lnk'); $s.TargetPath='%VENV%\Scripts\cfclient.exe'; $s.WorkingDirectory='%VENV%'; $s.Save()" >NUL 2>&1

echo.
echo ============================================================
echo  Done. Start cfclient from the "cfclient (ESP-Drone)" desktop
echo  shortcut, or run:  %VENV%\Scripts\cfclient.exe
echo ============================================================
pause
exit /b 0

:fail
echo.
echo Installation FAILED - read the message above.
pause
exit /b 1
