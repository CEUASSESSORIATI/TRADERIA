@echo off
setlocal
cd /d "%~dp0.."
echo ==========================================
echo   INSTALADOR - CEU TRADER INTELLIGENCE
echo ==========================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher nao encontrado. Instale Python 3.11 ou 3.12.
  exit /b 1
)
py -3.12 --version >nul 2>nul
if errorlevel 1 (
  py -3.11 --version >nul 2>nul
  if errorlevel 1 (
    echo Python 3.11/3.12 nao encontrado.
    exit /b 1
  )
  set PYTHON=py -3.11
) else (
  set PYTHON=py -3.12
)
if not exist ".venv" (
  %PYTHON% -m venv .venv
  if errorlevel 1 exit /b 1
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1
pip install -r requirements.txt
if errorlevel 1 exit /b 1
if not exist ".env" (
  copy ".env.example" ".env" >nul
  echo.
  echo Arquivo .env criado. Edite API_ACCESS_TOKEN antes de iniciar.
)
if not exist "data" mkdir data
python -m pytest
if errorlevel 1 (
  echo Testes falharam. Corrija os erros antes de iniciar o motor.
  exit /b 1
)
echo.
echo Instalacao e testes concluidos.
echo Configure .env e execute INICIAR_CEU_TRADER.bat
exit /b 0
