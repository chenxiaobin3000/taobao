@echo off
call clean.bat
call makemigrations.bat
call migrate.bat
python manage.py runserver