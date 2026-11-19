# Auditoria de prontidão — plano de execução

Status: preparação em andamento. Esta branch não é uma declaração de prontidão operacional.

## Etapas que serão executadas
- Revisar e corrigir o motor, paper broker, supervisor, API, worker, sincronização e outbox.
- Expandir testes unitários e de integração com mocks de mercado/cloud.
- Validar recuperação e persistência de estado e histórico.
- Rever SQL/RLS e o contrato entre backend e banco.
- Melhorar scripts Windows, configuração, logs e diagnóstico.
- Documentar instalação e operação DEMO.

## Guardrails
- Apenas paper trading.
- Não integrar nem enviar ordens a corretoras.
- Chaves e tokens nunca no frontend ou no Git.
- Não modificar o projeto G10 Intelligence.
- Não declarar testes de ambiente real/cloud como concluídos sem execução efetiva.

## Limitações de acesso
A aplicação do SQL no Lovable Cloud e a configuração de segredos no computador servidor exigem acesso/autorização nesse ambiente. A preparação local/repositório não comprova esses passos.
