from app.config import Settings
from app.models import Signal, StrategyName
from app.paper import PaperBroker


def test_paper_buy_and_sell_updates_cash_and_pnl():
    settings = Settings(paper_fee_pct=0, paper_slippage_pct=0, max_position_pct=50)
    broker = PaperBroker(settings)
    name = StrategyName.MODERATE
    buy = broker.execute(name, Signal.BUY, 100000)
    assert buy is not None
    assert broker.quantity[name] > 0
    sell = broker.execute(name, Signal.SELL, 110000)
    assert sell is not None
    assert broker.quantity[name] == 0
    assert broker.realized[name] > 0
    assert broker.snapshot(name, 110000).cash_brl > 100
