@echo off
call "%~dp0venv\Scripts\activate.bat"
if "%~1"=="" (
    cmd /k
) else (
    %*
)
