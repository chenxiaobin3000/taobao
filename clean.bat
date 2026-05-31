@echo off
rd /S /Q app\__pycache__
rd /S /Q app\migrations\__pycache__
rd /S /Q server\__pycache__

rd /S /Q app\models\__pycache__
rd /S /Q app\models\original\__pycache__
rd /S /Q app\models\system\__pycache__

rd /S /Q app\views\__pycache__
rd /S /Q app\views\original\__pycache__
rd /S /Q app\views\system\__pycache__
