@echo off
call backup.bat
call clean.bat
call makemigrations.bat
call migrate.bat
python manage.py runserver