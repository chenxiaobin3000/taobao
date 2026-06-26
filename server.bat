@echo off

for /d /r app %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)

python manage.py migrate
python manage.py makemigrations app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
