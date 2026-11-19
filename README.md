# CEU Trader Intelligence Engine

Demo-only bootstrap; no real orders or brokerage adapter. Includes FastAPI controls, simulated ticks, SQLite persistence and logs.

## Local run
1. `python -m venv .venv`
2. Activate `.venv` (Windows: `.venv\\Scripts\\activate`)
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --host 127.0.0.1 --port 8000`
5. Test: `pytest -q`

Persistent state and logs are created under `data/`. This demo is not yet a trading strategy or a live trading system.\n## Paper trader arena (experimental)\n\n- POST /paper/traders/tick: evaluates three independent virtual profiles (Momentum, Mean Reversion, Breakout).\n- GET /paper/traders/status: profile summaries.\n- POST /paper/moderator/tick: informational vote aggregation (WAIT/BUY/SELL/CONFLICT).\n- All responses are PAPER only. No broker connectivity, order placement or profitability claims.\n