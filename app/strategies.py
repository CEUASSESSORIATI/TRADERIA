from collections import deque
from app.models import Signal, StrategyDecision, StrategyName


class BaseStrategy:
    name: StrategyName
    fast_window: int
    slow_window: int
    min_change_pct: float

    def __init__(self) -> None:
        self.prices: deque[float] = deque(maxlen=240)

    def evaluate(self, price: float, has_position: bool) -> StrategyDecision:
        self.prices.append(price)
        if len(self.prices) < self.slow_window:
            return StrategyDecision(strategy=self.name, signal=Signal.HOLD, confidence=0.0,
                                    reason=f"Aguardando {self.slow_window} amostras de preço",
                                    price_brl=price)
        values = list(self.prices)
        fast = sum(values[-self.fast_window:]) / self.fast_window
        slow = sum(values[-self.slow_window:]) / self.slow_window
        spread_pct = (fast / slow - 1) * 100 if slow else 0
        if spread_pct >= self.min_change_pct and not has_position:
            return StrategyDecision(strategy=self.name, signal=Signal.BUY,
                                    confidence=min(0.95, 0.5 + abs(spread_pct) / 4),
                                    reason=f"Média curta acima da longa ({spread_pct:.3f}%)",
                                    price_brl=price)
        if spread_pct <= -self.min_change_pct and has_position:
            return StrategyDecision(strategy=self.name, signal=Signal.SELL,
                                    confidence=min(0.95, 0.5 + abs(spread_pct) / 4),
                                    reason=f"Média curta abaixo da longa ({spread_pct:.3f}%)",
                                    price_brl=price)
        return StrategyDecision(strategy=self.name, signal=Signal.HOLD, confidence=0.2,
                                reason=f"Sem cruzamento válido; diferença {spread_pct:.3f}%",
                                price_brl=price)


class ConservativeStrategy(BaseStrategy):
    name, fast_window, slow_window, min_change_pct = StrategyName.CONSERVATIVE, 8, 40, 0.35


class ModerateStrategy(BaseStrategy):
    name, fast_window, slow_window, min_change_pct = StrategyName.MODERATE, 5, 24, 0.22


class AggressiveStrategy(BaseStrategy):
    name, fast_window, slow_window, min_change_pct = StrategyName.AGGRESSIVE, 3, 12, 0.12


def build_strategies() -> dict[StrategyName, BaseStrategy]:
    return {
        StrategyName.CONSERVATIVE: ConservativeStrategy(),
        StrategyName.MODERATE: ModerateStrategy(),
        StrategyName.AGGRESSIVE: AggressiveStrategy(),
    }
