from dataclasses import dataclass
from app.config import Settings
from app.models import PortfolioSnapshot, StrategyDecision, Signal


@dataclass
class RiskVerdict:
    allowed: bool
    reason: str


class RiskSupervisor:
    """Hard risk controls. Protective sells remain allowed even after a halt."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def assess(self, decision: StrategyDecision, portfolio: PortfolioSnapshot) -> RiskVerdict:
        if decision.signal == Signal.HOLD:
            return RiskVerdict(False, "Sinal HOLD: nenhuma ordem")
        if decision.signal == Signal.SELL:
            if portfolio.btc_quantity <= 0:
                return RiskVerdict(False, "Não há posição para vender")
            return RiskVerdict(True, "Venda permitida para reduzir risco")
        if portfolio.halted:
            return RiskVerdict(False, "Estratégia suspensa pelo Supervisor")
        if portfolio.drawdown_pct >= self.settings.max_drawdown_pct:
            return RiskVerdict(False, "Limite máximo de drawdown atingido")
        loss_limit = portfolio.initial_capital_brl * self.settings.max_daily_loss_pct / 100
        if portfolio.daily_realized_pnl_brl <= -loss_limit:
            return RiskVerdict(False, "Limite de perda diária atingido")
        if decision.signal == Signal.BUY and portfolio.cash_brl <= 0:
            return RiskVerdict(False, "Saldo disponível insuficiente")
        if decision.signal == Signal.BUY and portfolio.btc_quantity * decision.price_brl >= (
            portfolio.equity_brl * self.settings.max_position_pct / 100
        ):
            return RiskVerdict(False, "Limite de exposição por posição atingido")
        return RiskVerdict(True, "Aprovado pelas regras de risco")
