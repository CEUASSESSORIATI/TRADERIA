# Operação

- Iniciar: `windows\INICIAR_CEU_TRADER.bat`
- Parar: `windows\PARAR_CEU_TRADER.bat`
- Verificar: `windows\VERIFICAR_CEU_TRADER.bat`
- Testes: `.venv\Scripts\python -m pytest`

O worker inicia junto com a API, executa ciclos de paper trading e tenta sincronizar a outbox. O intervalo padrão é 30 segundos. Sem credenciais de nuvem configuradas, os eventos permanecem na fila local. Observe os logs no terminal. Não use o sistema para ordens reais.
