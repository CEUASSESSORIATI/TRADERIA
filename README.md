# CEU Trader Intelligence

Motor independente de paper trading para Bitcoin (BTC/BRL), com três estratégias algorítmicas, Supervisor de risco, histórico e sincronização com Lovable Cloud.

## Estado atual

**Fundação técnica em desenvolvimento — DEMO apenas.** Este código não envia ordens a corretoras e não deve ser usado com dinheiro real.

- Três carteiras virtuais independentes, cada uma iniciando com R$ 100.
- Estratégias baseline por médias móveis (conservadora, moderada e agressiva).
- Supervisor com limites determinísticos de drawdown, perda realizada diária (fuso de Brasília), exposição e stop loss de 2% configurável.
- Cotação pública BTC/BRL via CoinGecko.
- Fila SQLite local usada exclusivamente como outbox técnica para sincronização; não substitui o banco de negócio no Lovable Cloud.
- Worker contínuo: executa ciclos de paper trading e sincroniza eventos pendentes com Lovable Cloud.
- Recuperação do saldo, posição, preço médio e limites a partir do último snapshot na nuvem; o motor permanece pausado se a nuvem não estiver configurada ou não puder recuperar o estado.
- API FastAPI com token Bearer.
- Scripts de instalação e operação para Windows 11.

## Requisitos

Windows 11 e Python 3.11 ou 3.12. Não requer Docker nem PostgreSQL local.

## Instalação

Clone a branch de desenvolvimento: `git clone -b development/ceu-trader-intelligence https://github.com/CEUASSESSORIATI/TRADERIA.git C:\\CEU-TRADER-INTELLIGENCE`.

1. Copie `.env.example` para `.env`.
2. Defina um `API_ACCESS_TOKEN` forte e exclusivo.
3. Execute `windows\INSTALAR_CEU_TRADER.bat`.
4. Consulte `docs/INSTALL_WINDOWS.md` e `docs/CONFIGURATION.md`.

## Endpoints

- `GET /health`: health check básico.
- `GET /status`: status protegido.
- `POST /engine/tick`: executa um ciclo DEMO protegido.
- `GET /portfolios`: carteiras virtuais.
- `GET /trades`: operações simuladas.

## Próximas etapas antes de considerar pronto

1. Confirmar o projeto Lovable Cloud de destino e aplicar `sql/lovable_cloud_schema.sql`.
2. Configurar URL e chave de serviço do Lovable Cloud no servidor.
3. Executar testes no Windows real e teste de integração com Lovable Cloud.
4. Validar os dashboards do Lovable com o contrato de API e os dados persistidos.
5. Validar operação contínua, reinicialização e recuperação após queda de rede.

Nenhuma rentabilidade é garantida. Estratégias e parâmetros são experimentais. A primeira versão serve para simulação e coleta de métricas, não para recomendação financeira.
