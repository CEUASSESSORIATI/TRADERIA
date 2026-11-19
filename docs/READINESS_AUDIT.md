# CEU Trader Intelligence — Auditoria de prontidão

## Escopo e segurança
- Exclusivamente paper trading BTC/BRL.
- Não conectar corretora nem habilitar ordens reais.
- Não alterar o repositório G10 Intelligence.
- Branch de trabalho: `audit/prepare-complete-papertrading`.

## Estado observado na branch `development/ceu-trader-intelligence`
- API FastAPI e endpoints básicos.
- Worker de ciclo contínuo.
- Três estratégias de médias móveis baseline.
- Broker de paper trading com saldo, posição, preço médio e P&L.
- Supervisor de risco com limites configuráveis.
- CoinGecko como provedor de preço.
- Outbox SQLite e sincronização REST com Lovable Cloud.
- SQL de tabelas de telemetria com RLS habilitado.
- Scripts de instalação e operação Windows.
- Testes unitários iniciais para broker, restore e risco.

## Pendências críticas de validação
1. Executar suíte de testes localmente em ambiente limpo.
2. Testar execução BUY/SELL, fees, slippage, preço médio, P&L e limites de posição.
3. Testar stop loss, limite de perda diária, drawdown e halt persistente.
4. Testar persistência e recuperação de todas as carteiras, trades, estado diário e halt.
5. Testar sincronização/outbox: falhas, reenvio, idempotência, duplicidade e ordenação.
6. Testar cotação: timeout, indisponibilidade, respostas inválidas e preço stale.
7. Testar ciclo e API concurrentemente, shutdown e reinicialização.
8. Aplicar SQL no projeto Lovable Cloud correto e confirmar esquema, RLS e acesso backend.
9. Configurar secrets apenas no servidor Windows, nunca no frontend ou Git.
10. Validar operação contínua e logs/alertas.

## Riscos detectados na leitura estática
- O histórico de trades é apenas memória do processo e não é reconstituído na recuperação do broker.
- A sincronização REST e a outbox precisam de validação de idempotência/duplicidade e ordenação.
- O motor depende da recuperação cloud, mas precisa de testes para cenários de snapshot ausente ou incompleto.
- O worker, atualmente, não oferece controles administrativos completos nem monitoramento dedicado.
- Estratégias são regras determinísticas de médias móveis; não são agentes adaptativos.
- Frontend completo não está presente nesta branch.
- A suíte existente é pequena e não prova prontidão operacional.

## Critério para liberação DEMO
Só considerar o motor pronto para operação contínua DEMO após todos os testes críticos acima passarem, integração cloud comprovada, secrets configurados no host e observação de execução sem inconsistências. Este projeto não deve enviar ordens reais.
