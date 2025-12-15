@echo off
rd /S /Q app\__pycache__
del /S /Q app\__init__.py
rd /S /Q app\migrations\__pycache__
del /S /Q app\migrations\__init__.py
rd /S /Q server\__pycache__
del /S /Q server\__init__.py

rd /S /Q app\models\__pycache__
del /S /Q app\models\__init__.py
rd /S /Q app\models\original\__pycache__
del /S /Q app\models\original\__init__.py
rd /S /Q app\models\system\__pycache__
del /S /Q app\models\system\__init__.py

rd /S /Q app\views\__pycache__
del /S /Q app\views\__init__.py
rd /S /Q app\views\original\__pycache__
del /S /Q app\views\original\__init__.py
rd /S /Q app\views\system\__pycache__
del /S /Q app\views\system\__init__.py
