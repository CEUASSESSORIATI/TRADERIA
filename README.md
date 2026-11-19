# CEU Trader Intelligence Engine

Paper trading engine bootstrap. **Demo-only; no real orders.**

## Modules
- API (FastAPI)
- Risk guardrails and simulator
- Three independent demo strategies
- Local desktop control planned as next milestone

Run: `python -m venv .venv`, activate, `pip install -r requirements.txt`, `uvicorn app.main:app --host 127.0.0.1 --port 8000`.
