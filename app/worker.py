import asyncio
import logging
from app.cloud import CloudSync
from app.config import Settings
from app.engine import TradingEngine
from app.sync import OutboxSynchronizer

log = logging.getLogger(__name__)


async def run_worker(engine: TradingEngine, settings: Settings) -> None:
    sync = OutboxSynchronizer(engine.outbox, CloudSync(settings))
    while True:
        try:
            await engine.tick()
        except Exception as exc:
            engine.last_error = str(exc)
            log.exception("Trading cycle failed; next cycle will retry")
        try:
            await sync.flush()
        except Exception:
            log.exception("Outbox sync failed; events remain queued")
        await asyncio.sleep(max(5, settings.trading_cycle_seconds))
