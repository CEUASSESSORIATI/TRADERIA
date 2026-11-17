# Configuração

1. Copie `.env.example` para `.env`.
2. Gere um token aleatório longo para `API_ACCESS_TOKEN`.
3. Mantenha `TRADING_MODE=paper`.
4. `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` só devem ser preenchidos após confirmar os dados do projeto Lovable Cloud correto.
5. Nunca envie `.env` ao GitHub, nem compartilhe a service role key em chats ou capturas de tela.

O prefixo padrão das tabelas é `cti_`. O SQL cria tabelas com esse prefixo. A cotação vem do endpoint público CoinGecko e pode estar sujeita a limites e indisponibilidade.
