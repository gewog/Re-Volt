@echo off
cd /d "%~dp0"
set DJANGO_DEBUG=1
echo Установка зависимостей...
venv\Scripts\pip.exe install django-extensions Werkzeug pyOpenSSL -q 2>nul
if not exist staticfiles mkdir staticfiles
venv\Scripts\python.exe manage.py collectstatic --noinput 2>nul
echo.
echo Запуск сервера по HTTPS: https://127.0.0.1:8000/
echo Браузер откроется через 4 секунды. При первом заходе: Дополнительно - Перейти на сайт
echo.
start /b cmd /c "timeout /t 4 /nobreak >nul && start https://127.0.0.1:8000/"
venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
if errorlevel 1 (
  echo.
  echo HTTPS не запустился. Запуск по HTTP...
  echo Откройте в браузере: http://127.0.0.1:8000/
  start /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000/"
  venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000 --no-https
)
pause
