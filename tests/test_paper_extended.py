import pytest
from app.config import Settings
from app.models import Signal, StrategyName
from app.paper import PaperBroker


def test_buy_respects_max_position_and_fees():
    s = Settings(paper_fee_pct=1, paper_slippage_pct=0, max_position_pct=25)
    b = PaperBroker(s)
    t = b.execute(StrategyName.CONSERVATIVE, Signal.BUY, 100000)
    assert t
    assert t.gross_brl == pytest.approx(25)
    assert t.fee_brl == pytest.approx(.25)
    assert b.cash[StrategyName.CONSERVATIVE] == pytest.approx(75)
    assert b.quantity[StrategyName.CONSERVATIVE] == pytest.approx(24.75/100000)


def test_sell_fee_and_realized_pnl_are_applied():
    s = Settings(paper_fee_pct=1, paper_slippage_pct=0, max_position_pct=100)
    b = PaperBroker(s)
    n = StrategyName.MODERATE
    b.execute(n, Signal.BUY, 100000)
    t = b.execute(n, Signal.SELL, 110000)
    assert t
    assert t.fee_brl > 0
    assert t.realized_pnl_brl > 0
    assert b.quantity[n] == 0
    assert b.cash[n] > 100


def test_cannot_sell_without_position():
    b = PaperBroker(Settings())
    assert b.execute(StrategyName.AGGRESSIVE, Signal.SELL, 100000) is None


def test_multiple_buy_average_entry_is_weighted():
    s = Settings(paper_fee_pct=0, paper_slippage_pct=0, max_position_pct=100)
    b = PaperBroker(s)
    n = StrategyName.CONSERVATIVE
    b.cash[n] = 200
    b.execute(n, Signal.BUY, 100)
    b.execute(n, Signal.BUY, 200)
    assert b.avg_entry[n] == pytest.approx(133.3333333333)
