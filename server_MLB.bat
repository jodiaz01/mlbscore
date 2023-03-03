@echo off

color 2
echo.

cd mlbapp/scripts
call activate.bat
cd..
cd..
#start call  python manage.py runserver 127.0.0.1:8000
start call  python manage.py runserver 172.21.0.4:8000
#start call  python manage.py runserver 10.0.0.16:8000

echo.










