@echo off
for /d /r app %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)
