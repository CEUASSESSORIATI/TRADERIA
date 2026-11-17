@echo off
setlocal
cd /d "%~dp0.."
echo Faça backup do .env e da pasta data antes de atualizar.
git pull
if errorlevel 1 exit /b 1
call .venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 exit /b 1
python -m pytest
