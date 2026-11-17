import hmac
import logging
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Header, HTTPException
from app.config import get_settings
from app.engine import TradingEngine

settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO),
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
engine: TradingEngine | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    engine = TradingEngine(settings)
    yield
    engine = None


app = FastAPI(title="CEU Trader Intelligence API", version="0.1.0",
              description="Motor DEMO de paper trading; não envia ordens reais.",
              lifespan=lifespan)


async def require_token(authorization: str | None = Header(default=None)):
    if settings.api_access_token == "CHANGE_ME_TO_A_LONG_RANDOM_SECRET":
        raise HTTPException(status_code=503, detail="Configure API_ACCESS_TOKEN no .env")
    expected = f"Bearer {settings.api_access_token}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="Não autorizado")


@app.get("/health")
async def health():
    return {"status": "ok", "mode": "paper", "cloud_configured": settings.cloud_configured}


@app.get("/status", dependencies=[Depends(require_token)])
async def status():
    if engine is None:
        raise HTTPException(status_code=503, detail="Motor não inicializado")
    return {
        "mode": "paper", "cycles": engine.cycles, "last_price_brl": engine.last_price,
        "last_error": engine.last_error, "pending_cloud_events": engine.outbox.count(),
        "cloud_configured": settings.cloud_configured,
    }


@app.post("/engine/tick", dependencies=[Depends(require_token)])
async def run_tick():
    if engine is None:
        raise HTTPException(status_code=503, detail="Motor não inicializado")
    try:
        return await engine.tick()
    except Exception as exc:
        engine.last_error = str(exc)
        logging.getLogger(__name__).exception("Trading tick failed")
        raise HTTPException(status_code=502, detail="Falha ao executar ciclo; consulte os logs") from exc


@app.get("/portfolios", dependencies=[Depends(require_token)])
async def portfolios():
    if engine is None or engine.last_price is None:
        return {"items": [], "message": "Aguardando primeira cotação"}
    from app.models import StrategyName
    return {"items": [engine.broker.snapshot(name, engine.last_price).model_dump(mode="json")
                      for name in StrategyName]}


@app.get("/trades", dependencies=[Depends(require_token)])
async def trades():
    if engine is None:
        return {"items": []}
    return {"items": [trade.model_dump(mode="json") for trade in engine.broker.trades]}
