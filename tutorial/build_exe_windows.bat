@echo off
setlocal

REM Build tutorial_refac_win.py into a Windows exe using PyInstaller.
REM Run this script from Windows (double-click or cmd).

cd /d "%~dp0"

py -3 -m pip install --upgrade pip pyinstaller
if errorlevel 1 goto :fail

py -3 -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onefile ^
  --name tutorial_refac_win ^
  --collect-submodules psychopy ^
  --add-data "erp_stimuli;erp_stimuli" ^
  --add-data "main_stimuli;main_stimuli" ^
  tutorial_refac_win.py
if errorlevel 1 goto :fail

echo.
echo Build completed.
echo EXE path: %~dp0dist\tutorial_refac_win.exe
exit /b 0

:fail
echo.
echo Build failed.
exit /b 1

