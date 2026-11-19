# CEU Trader Intelligence Engine

Bootstrap seguro para paper trading. Não envia ordens reais.

## Execução
Python 3.11+: `pip install -r requirements.txt`, `uvicorn app.main:app --reload`.

## API
- GET `/health`
- GET `/status`
- POST `/paper/tick` (simulação determinística)

O projeto começa em DEMO. Integrações com corretora e execução real não estão habilitadas.