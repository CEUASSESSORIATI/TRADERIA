from app.config import Settings
from app.models import PortfolioSnapshot, Signal, StrategyDecision, StrategyName
from app.risk import RiskSupervisor


def _portfolio(**kw):
    base = dict(strategy=StrategyName.MODERATE, initial_capital_brl=100, cash_brl=50,
        btc_quantity=0.0001, avg_entry_brl=300000, equity_brl=80,
        realized_pnl_brl=0, daily_realized_pnl_brl=0, unrealized_pnl_brl=-20,
        return_pct=-20, peak_equity_brl=100, drawdown_pct=20, halted=False)
    base.update(kw)
    return PortfolioSnapshot(**base)


def _decision(signal, price=300000):
    return StrategyDecision(strategy=StrategyName.MODERATE, signal=signal, confidence=.8,
        reason="test", price_brl=price)


def test_drawdown_blocks_buy():
    verdict = RiskSupervisor(Settings(max_drawdown_pct=8)).assess(_decision(Signal.BUY),
        _portfolio(drawdown_pct=8))
    assert not verdict.allowed
    assert "drawdown" in verdict.reason.lower()


def test_exposure_limit_blocks_buy():
    settings = Settings(max_position_pct=25)
    p = _portfolio(btc_quantity=0.0001, equity_brl=100, cash_brl=90)
    verdict = RiskSupervisor(settings).assess(_decision(Signal.BUY), p)
    assert not verdict.allowed
    assert "exposição" in verdict.reason.lower()


def test_sell_is_allowed_for_protection():
    p = _portfolio(halted=True, daily_realized_pnl_brl=-99)
    verdict = RiskSupervisor(Settings()).assess(_decision(Signal.SELL), p)
    assert verdict.allowed


def test_buy_is_blocked_after_daily_limit():
    settings = Settings(max_daily_loss_pct=3)
    p = _portfolio(daily_realized_pnl_brl=-3.01, halted=False)
    verdict = RiskSupervisor(settings).assess(_decision(Signal.BUY), p)
    assert not verdict.allowed
