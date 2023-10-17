@echo off

setlocal enabledelayedexpansion
set "script_dir=%~dp0"
set "project_dir="

:search_loop
if exist "%script_dir%manage.py" (
    set "project_dir=%script_dir%"
) else (
    set "script_dir=!script_dir:~0,-1!"
    if "!script_dir!" == "" goto :search_end
    goto :search_loop
)

:search_end
if "%project_dir%" == "" (
    echo manage.py not found in this directory or any parent directory.
    exit /b
)

cd /d "%project_dir%"
start pip install -r requirements.txt
timeout /t 30
start python manage.py runserver
start "" http://127.0.0.1:8000/
