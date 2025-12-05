rd /S /Q ..\static\css
rd /S /Q ..\static\fonts
rd /S /Q ..\static\img
rd /S /Q ..\static\js
del /F /Q ..\app\templates\index.html
npm run build
xcopy .\dist\static\* ..\static /E /Q /Y
copy .\dist\index.html ..\app\templates\ /Y
