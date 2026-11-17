import asyncio
import logging
from app.config import Settings
from app.models import StrategyName
from app.market import CoinGeckoPriceProvider
from app.paper import PaperBroker
from app.risk import RiskSupervisor
from app.strategies import build_strategies
from app.outbox import Outbox

log = logging.getLogger(__name__)


class TradingEngine:
    def __init__(self, settings: Settings) -> None:
        if settings.trading_mode.lower() != "paper":
            raise ValueError("Este build aceita exclusivamente TRADING_MODE=paper")
        self.settings = settings
        self.market = CoinGeckoPriceProvider(settings.coingecko_demo_api_key)
        self.broker = PaperBroker(settings)
        self.supervisor = RiskSupervisor(settings)
        self.strategies = build_strategies()
        self.outbox = Outbox(settings.outbox_path)
        self.last_price: float | None = None
        self.last_error: str | None = None
        self.cycles = 0
        self._cycle_lock = asyncio.Lock()

    async def tick(self) -> dict:
        async with self._cycle_lock:
            return await self._tick_unlocked()

    async def _tick_unlocked(self) -> dict:
        quote = await self.market.get_btc_brl()
        self.last_price = quote.price_brl
        self.last_error = None
        self.cycles += 1
        results = []
        self.outbox.enqueue("market_quote", quote.model_dump(mode="json"))
        for name in StrategyName:
            before = self.broker.snapshot(name, quote.price_brl)
            decision = self.strategies[name].evaluate(
                quote.price_brl, has_position=before.btc_quantity > 0
            )
            verdict = self.supervisor.assess(decision, before)
            if not verdict.allowed and verdict.reason in (
                "Limite máximo de drawdown atingido", "Limite de perda diária atingido"
            ):
                self.broker.halted[name] = True
            trade = None
            if verdict.allowed:
                trade = self.broker.execute(name, decision.signal, quote.price_brl)
                if trade:
                    self.outbox.enqueue("paper_trade", trade.model_dump(mode="json"))
            snapshot = self.broker.snapshot(name, quote.price_brl)
            self.outbox.enqueue("strategy_snapshot", snapshot.model_dump(mode="json"))
            self.outbox.enqueue("strategy_decision", {
                **decision.model_dump(mode="json"), "risk_allowed": verdict.allowed,
                "risk_reason": verdict.reason,
            })
            results.append({
                "strategy": name.value, "decision": decision.model_dump(mode="json"),
                "risk": {"allowed": verdict.allowed, "reason": verdict.reason},
                "trade": trade.model_dump(mode="json") if trade else None,
                "portfolio": snapshot.model_dump(mode="json"),
            })
        log.info("Trading cycle %s complete at BRL %.2f", self.cycles, quote.price_brl)
        return {"cycle": self.cycles, "quote": quote.model_dump(mode="json"), "strategies": results}
