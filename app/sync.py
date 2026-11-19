import logging
from app.cloud import CloudSync
from app.outbox import Outbox

log = logging.getLogger(__name__)
TABLES = {"market_quote":"market_quotes","paper_trade":"paper_trades",
          "strategy_snapshot":"strategy_snapshots","strategy_decision":"strategy_decisions"}


class OutboxSynchronizer:
    def __init__(self, outbox: Outbox, cloud: CloudSync) -> None:
        self.outbox, self.cloud = outbox, cloud

    async def flush(self, limit: int = 100) -> int:
        if not self.cloud.settings.cloud_configured:
            return 0
        delivered = 0
        for event_id, event_type, payload in self.outbox.pending(limit):
            table = TABLES.get(event_type)
            if table is None:
                log.error("Unknown outbox event type: %s", event_type)
                continue
            try:
                await self.cloud.insert(table, payload)
            except Exception:
                log.exception("Cloud sync failed for event %s; will retry", event_id)
                break
            self.outbox.acknowledge(event_id)
            delivered += 1
        return delivered

    async def restore_portfolios(self, broker) -> int:
        from app.models import StrategyName
        restored = 0
        for strategy in StrategyName:
            state = await self.cloud.fetch_latest_snapshot(strategy.value)
            if state:
                broker.restore(state)
                restored += 1
        return restored
