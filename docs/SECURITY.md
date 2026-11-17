# Segurança

- Nunca commitar `.env`, tokens ou chaves.
- API vinculada a `127.0.0.1` por padrão.
- Endpoints operacionais exigem Bearer token.
- `/health` retorna apenas estado básico.
- Service role do Lovable Cloud é segredo administrativo e só pode ficar no backend.
- RLS fica habilitado nas tabelas de telemetria; não criar policies públicas.
- Não expor a API à internet antes de configurar TLS/túnel e controles de acesso.
- O projeto não implementa execução financeira real.
