import asyncio
import logging
from app.cloud import CloudSync
from app.config import Settings
from app.engine import TradingEngine
from app.models import StrategyName
from app.sync import OutboxSynchronizer

log = logging.getLogger(__name__)


async def run_worker(engine: TradingEngine, settings: Settings) -> None:
    sync = OutboxSynchronizer(engine.outbox, CloudSync(settings))
    restored = False
    expected = len(StrategyName)
    while True:
        if not settings.cloud_configured:
            log.warning("Lovable Cloud não configurado; motor pausado para proteger a continuidade das carteiras.")
            await asyncio.sleep(15)
            continue
        if not restored:
            try:
                while engine.outbox.count() > 0:
                    delivered = await sync.flush()
                    if delivered == 0:
                        raise RuntimeError("Outbox não foi totalmente sincronizada; recuperação pausada")
                count = await sync.restore_portfolios(engine.broker)
                # A clean installation may have no snapshots. A partial recovery is unsafe:
                # it would silently mix recovered and freshly initialized portfolios.
                if 0 < count < expected:
                    raise RuntimeError(
                        f"Recuperação incompleta ({count}/{expected} carteiras); "
                        "motor permanece pausado para evitar estado inconsistente."
                    )
                if count not in (0, expected):
                    raise RuntimeError(f"Quantidade inesperada de carteiras recuperadas: {count}/{expected}")
                log.info("Cloud portfolio recovery complete; restored %s/%s strategies", count, expected)
                restored = True
            except Exception:
                log.exception("Cloud recovery unavailable or incomplete; trading remains paused")
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
