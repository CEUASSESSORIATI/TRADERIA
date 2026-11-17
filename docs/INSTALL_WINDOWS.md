# Instalação no Windows 11

Requisitos: Windows 11 e Python 3.11 ou 3.12 com Python Launcher (`py`). Não instala Docker, WSL nem PostgreSQL.

1. Altere a visibilidade do repositório para **Private** antes de clonar, conforme combinado.
2. Clone a branch de desenvolvimento: `git clone -b development/ceu-trader-intelligence https://github.com/CEUASSESSORIATI/TRADERIA.git C:\CEU-TRADER-INTELLIGENCE`.
3. Copie `.env.example` para `.env` e configure um token forte em `API_ACCESS_TOKEN`.
4. Execute `windows\INSTALAR_CEU_TRADER.bat`.
5. Inicie com `windows\INICIAR_CEU_TRADER.bat`.
6. Verifique com `windows\VERIFICAR_CEU_TRADER.bat`; pare com `windows\PARAR_CEU_TRADER.bat`.

O instalador cria um ambiente virtual, instala dependências e executa os testes automatizados. Não registra serviço ou tarefa agendada nesta etapa; isso será acrescentado depois de validar a execução na máquina real.
