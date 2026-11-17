from uuid import uuid4
from datetime import datetime
from zoneinfo import ZoneInfo
from app.config import Settings
from app.models import PaperTrade, PortfolioSnapshot, StrategyName, Signal


class PaperBroker:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.cash = {name: settings.initial_capital_brl for name in StrategyName}
        self.quantity = {name: 0.0 for name in StrategyName}
        self.avg_entry = {name: 0.0 for name in StrategyName}
        self.realized = {name: 0.0 for name in StrategyName}
        self.daily_realized = {name: 0.0 for name in StrategyName}
        self.current_day = datetime.now(ZoneInfo('America/Sao_Paulo')).date()
        self.peak = {name: settings.initial_capital_brl for name in StrategyName}
        self.halted = {name: False for name in StrategyName}
        self.trades: list[PaperTrade] = []

    def _roll_day(self) -> None:
        today = datetime.now(ZoneInfo('America/Sao_Paulo')).date()
        if today != self.current_day:
            self.daily_realized = {name: 0.0 for name in StrategyName}
            self.current_day = today

    def snapshot(self, name: StrategyName, price: float) -> PortfolioSnapshot:
        self._roll_day()
        qty = self.quantity[name]
        equity = self.cash[name] + qty * price
        self.peak[name] = max(self.peak[name], equity)
        drawdown = max(0.0, (self.peak[name] - equity) / self.peak[name] * 100)
        unrealized = (price - self.avg_entry[name]) * qty
        return PortfolioSnapshot(
            strategy=name, initial_capital_brl=self.settings.initial_capital_brl,
            cash_brl=round(self.cash[name], 8), btc_quantity=qty,
            avg_entry_brl=round(self.avg_entry[name], 8), equity_brl=round(equity, 8),
            realized_pnl_brl=round(self.realized[name], 8),
            daily_realized_pnl_brl=round(self.daily_realized[name], 8),
            unrealized_pnl_brl=round(unrealized, 8),
            return_pct=round((equity / self.settings.initial_capital_brl - 1) * 100, 4),
            peak_equity_brl=self.peak[name], drawdown_pct=round(drawdown, 4),
            halted=self.halted[name],
        )

    def execute(self, name: StrategyName, signal: Signal, price: float) -> PaperTrade | None:
        if signal not in (Signal.BUY, Signal.SELL):
            return None
        fee_rate = self.settings.paper_fee_pct / 100
        slip_rate = self.settings.paper_slippage_pct / 100
        if signal == Signal.BUY:
            execution_price = price * (1 + slip_rate)
            budget = min(self.cash[name], self.settings.initial_capital_brl *
                         self.settings.max_position_pct / 100)
            if budget <= 0:
                return None
            fee = budget * fee_rate
            qty = (budget - fee) / execution_price
            self.cash[name] -= budget
            old_qty = self.quantity[name]
            self.avg_entry[name] = ((self.avg_entry[name] * old_qty) + budget) / (old_qty + qty)
            self.quantity[name] += qty
            trade = PaperTrade(id=str(uuid4()), strategy=name, side="buy", symbol="BTCBRL",
                               quantity=qty, price_brl=execution_price, gross_brl=budget,
                               fee_brl=fee, slippage_brl=budget * slip_rate)
        else:
            qty = self.quantity[name]
            if qty <= 0:
                return None
            execution_price = price * (1 - slip_rate)
            gross = qty * execution_price
            fee = gross * fee_rate
            pnl = (execution_price - self.avg_entry[name]) * qty - fee
            self.cash[name] += gross - fee
            self.realized[name] += pnl
            self._roll_day()
            self.daily_realized[name] += pnl
            self.quantity[name] = 0.0
            self.avg_entry[name] = 0.0
            trade = PaperTrade(id=str(uuid4()), strategy=name, side="sell", symbol="BTCBRL",
                               quantity=qty, price_brl=execution_price, gross_brl=gross,
                               fee_brl=fee, slippage_brl=gross * slip_rate, realized_pnl_brl=pnl)
        self.trades.append(trade)
        return trade

    def restore(self, state: dict) -> None:
        """Restore authoritative portfolio state from the latest Lovable Cloud snapshot."""
        name = StrategyName(state["strategy"])
        self.cash[name] = float(state["cash_brl"])
        self.quantity[name] = float(state["btc_quantity"])
        self.avg_entry[name] = float(state["avg_entry_brl"])
        self.realized[name] = float(state["realized_pnl_brl"])
        self.daily_realized[name] = float(state["daily_realized_pnl_brl"])
        self.peak[name] = float(state["peak_equity_brl"])
        self.halted[name] = bool(state["halted"])
