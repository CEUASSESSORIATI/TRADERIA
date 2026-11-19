# Conexão com Lovable Cloud

A integração usa a API REST compatível com Supabase, executada exclusivamente pelo backend Python.

1. Confirme que o projeto Lovable Cloud de destino é o correto.
2. Execute `sql/lovable_cloud_schema.sql` no SQL Editor desse projeto.
3. No arquivo `.env` do Windows, configure `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY`.
4. Mantenha a chave fora do frontend, fora do GitHub e fora de mensagens.
5. Reinicie a API e confirme em `/status` que `cloud_configured` está true.
6. A fila técnica local será enviada automaticamente quando a nuvem estiver configurada e disponível.
7. No início do processo, o backend sincroniza eventos pendentes e recupera o último snapshot de cada carteira antes de liberar novos ciclos. Se não conseguir recuperar o estado, o motor permanece pausado.

A chave service role concede privilégios elevados. Guarde-a somente no servidor. O prefixo de tabelas é `cti_`.

A migration cria tabelas com RLS habilitado e sem políticas públicas. A gravação é feita pela service role no servidor. A leitura pelos dashboards deve usar políticas/autenticação apropriadas; não habilite acesso anon amplo.
