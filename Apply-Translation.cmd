@echo off
setlocal
cd /d "%~dp0"
set "PYTHONHOME=%~dp0Runtime\Python315"
"%PYTHONHOME%\python.exe" "%~dp0Apply-Translation.py"
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" echo A traducao nao foi aplicada. Consulte a mensagem acima.
pause
exit /b %RESULT%
