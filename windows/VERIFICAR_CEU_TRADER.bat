@echo off
curl --fail --silent http://127.0.0.1:8787/health
if errorlevel 1 (
  echo.
  echo API indisponivel em 127.0.0.1:8787
  exit /b 1
)
echo.
