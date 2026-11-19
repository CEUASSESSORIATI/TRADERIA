# API

Base local: `http://127.0.0.1:8787`

| Método | Rota | Proteção | Finalidade |
|---|---|---|---|
| GET | /health | Não | Estado básico do processo |
| GET | /status | Bearer | Ciclos, preço e fila pendente |
| POST | /engine/tick | Bearer | Executar um ciclo manual |
| GET | /portfolios | Bearer | Carteiras DEMO |
| GET | /trades | Bearer | Operações simuladas |

Exemplo PowerShell:

```powershell
$token = "SEU_TOKEN_LOCAL"
Invoke-RestMethod -Headers @{ Authorization = "Bearer $token" } http://127.0.0.1:8787/status
```

Não exponha a API publicamente sem TLS, autenticação forte e regras de rede adequadas.
