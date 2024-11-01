:: start_django.bat
@echo off
SET "VENV_PATH=C:\python\.venv"
SET "DJANGO_PROJECT_PATH=C:\projects\welding_data\"


REM 가상환경 활성화
CALL %VENV_PATH%\Scripts\activate.bat

REM Django 서버 실행
start cmd /k "cd %DJANGO_PROJECT_PATH% && python manage.py runserver"

REM 하위 스크립트 실행 (로그를 프롬프트에 표시)
start cmd /k "cd %DJANGO_PROJECT_PATH% && python polling_data.py"