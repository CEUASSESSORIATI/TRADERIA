# Arquitetura

- **Lovable:** interface, dashboards e experiência do usuário.
- **Lovable Cloud:** banco PostgreSQL gerenciado e autenticação do produto.
- **Windows 11:** processo Python/FastAPI, fonte de preços, três estratégias, Supervisor e paper broker.
- **Outbox local SQLite:** buffer durável de eventos ainda não enviados. É infraestrutura de entrega, não banco de negócio. O estado oficial das carteiras é recuperado do Lovable Cloud.

## Ciclo DEMO

1. Consultar preço BTC/BRL.
2. Alimentar cada estratégia independente.
3. Gerar sinal explicável (BUY/SELL/HOLD).
4. Passar sinal pelo Supervisor determinístico.
5. Executar somente no broker simulado.
6. Registrar decisão, trade e snapshot na outbox.
7. Sincronizar eventos pendentes com Lovable Cloud.

## Limites

O processo só aceita `TRADING_MODE=paper`. Não há adaptador de corretora nem endpoint de ordem real. A service role, quando configurada, existe apenas no servidor Windows e nunca no frontend ou no GitHub.
