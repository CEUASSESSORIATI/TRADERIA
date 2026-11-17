import asyncio
import logging
from app.cloud import CloudSync
from app.config import Settings
from app.engine import TradingEngine
from app.sync import OutboxSynchronizer

log = logging.getLogger(__name__)


async def run_worker(engine: TradingEngine, settings: Settings) -> None:
    sync = OutboxSynchronizer(engine.outbox, CloudSync(settings))
    restored = False
    while True:
        if not settings.cloud_configured:
            log.warning("Lovable Cloud não configurado; motor pausado para proteger a continuidade das carteiras.")
            await asyncio.sleep(15)
            continue
        if not restored:
            try:
                await sync.flush()
                count = await sync.restore_portfolios(engine.broker)
                log.info("Cloud portfolio recovery complete; restored %s strategies", count)
                restored = True
            except Exception:
                log.exception("Cloud recovery unavailable; trading remains paused")
                await asyncio.sleep(15)
                continue
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
