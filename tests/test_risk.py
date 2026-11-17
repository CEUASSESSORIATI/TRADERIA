from app.config import Settings
from app.models import PortfolioSnapshot, Signal, StrategyDecision, StrategyName
from app.risk import RiskSupervisor


def portfolio(**overrides):
    data = dict(strategy=StrategyName.CONSERVATIVE, initial_capital_brl=100, cash_brl=100,
                btc_quantity=0, equity_brl=100, realized_pnl_brl=0, daily_realized_pnl_brl=0,
                unrealized_pnl_brl=0, return_pct=0, peak_equity_brl=100,
                drawdown_pct=0, halted=False)
    data.update(overrides)
    return PortfolioSnapshot(**data)


def test_hold_is_not_executable():
    decision = StrategyDecision(strategy=StrategyName.CONSERVATIVE, signal=Signal.HOLD,
                                 confidence=0.1, reason="test", price_brl=300000)
    assert not RiskSupervisor(Settings()).assess(decision, portfolio()).allowed


def test_halted_strategy_is_blocked():
    decision = StrategyDecision(strategy=StrategyName.CONSERVATIVE, signal=Signal.BUY,
                                 confidence=0.8, reason="test", price_brl=300000)
    verdict = RiskSupervisor(Settings()).assess(decision, portfolio(halted=True))
    assert not verdict.allowed
