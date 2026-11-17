from datetime import datetime, timezone
from enum import StrEnum
from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StrategyName(StrEnum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class Signal(StrEnum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class PriceSnapshot(BaseModel):
    symbol: str
    price_brl: float = Field(gt=0)
    source: str
    observed_at: datetime = Field(default_factory=utc_now)


class StrategyDecision(BaseModel):
    strategy: StrategyName
    signal: Signal
    confidence: float = Field(ge=0, le=1)
    reason: str
    price_brl: float
    created_at: datetime = Field(default_factory=utc_now)


class PaperTrade(BaseModel):
    id: str
    strategy: StrategyName
    side: str
    symbol: str
    quantity: float
    price_brl: float
    gross_brl: float
    fee_brl: float
    slippage_brl: float
    realized_pnl_brl: float = 0
    created_at: datetime = Field(default_factory=utc_now)


class PortfolioSnapshot(BaseModel):
    strategy: StrategyName
    initial_capital_brl: float
    cash_brl: float
    btc_quantity: float
    equity_brl: float
    realized_pnl_brl: float
    unrealized_pnl_brl: float
    return_pct: float
    peak_equity_brl: float
    drawdown_pct: float
    halted: bool = False
