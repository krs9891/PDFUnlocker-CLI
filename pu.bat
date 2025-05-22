@echo off
:: Get the folder where this .bat file lives
set script_dir=%~dp0

:: Optional: activate venv if present
if exist "%script_dir%\.venv\Scripts\activate" (
    call "%script_dir%\.venv\Scripts\activate"
)

:: Run the script from the same folder, pass through all args
py "%script_dir%pdf_unlocker.py" %*
