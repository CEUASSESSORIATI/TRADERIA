import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.models import StrategyName
from app.worker import run_worker


class DummyEngine:
    def __init__(self):
        self.outbox = MagicMock()
        self.outbox.count.return_value = 0
        self.broker = MagicMock()
        self.tick = AsyncMock()


@pytest.mark.parametrize("count", [1, 2])
def test_partial_cloud_recovery_does_not_trade(count):
    engine = DummyEngine()
    settings = MagicMock()
    settings.cloud_configured = True
    settings.trading_cycle_seconds = 5
    sync = MagicMock()
    sync.flush = AsyncMock(return_value=0)
    sync.restore_portfolios = AsyncMock(return_value=count)

    async def stop_sleep(_):
        raise asyncio.CancelledError

    with patch("app.worker.OutboxSynchronizer", return_value=sync), \
         patch("app.worker.CloudSync"), \
         patch("app.worker.asyncio.sleep", side_effect=stop_sleep):
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(run_worker(engine, settings))
    engine.tick.assert_not_called()


def test_complete_recovery_proceeds_to_tick():
    engine = DummyEngine()
    settings = MagicMock()
    settings.cloud_configured = True
    settings.trading_cycle_seconds = 5
    sync = MagicMock()
    sync.flush = AsyncMock(return_value=0)
    sync.restore_portfolios = AsyncMock(return_value=len(StrategyName))

    async def stop_after_tick(_):
        raise asyncio.CancelledError

    with patch("app.worker.OutboxSynchronizer", return_value=sync), \
         patch("app.worker.CloudSync"), \
         patch("app.worker.asyncio.sleep", side_effect=stop_after_tick):
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(run_worker(engine, settings))
    engine.tick.assert_awaited_once()
