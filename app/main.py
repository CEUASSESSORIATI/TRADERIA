from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="CEU Trader Intelligence Engine", version="0.1.0", description="Paper-trading bootstrap; no live orders.")

class TickRequest(BaseModel):
    symbol: str = Field(default="BTCUSDT", min_length=3, max_length=20)
    price: float = Field(gt=0)

@app.get("/health")
def health():
    return {"ok": True, "mode": "DEMO"}

@app.get("/status")
def status():
    return {"engine": "ready", "mode": "DEMO", "live_orders_enabled": False}

@app.post("/paper/tick")
def paper_tick(req: TickRequest):
    return {"symbol": req.symbol.upper(), "price": req.price, "mode": "DEMO", "decision": "observe", "live_order": False}
