from collections import deque
from dataclasses import dataclass, field

@dataclass
class TraderProfile:
    name: str
    strategy: str
    capital: float = 100.0
    risk_pct: float = 0.01
    history: deque = field(default_factory=lambda: deque(maxlen=30))
    signals: list = field(default_factory=list)

    def evaluate(self, symbol: str, price: float):
        self.history.append(price)
        decision = "HOLD"
        if len(self.history) >= 3:
            vals=list(self.history)
            if self.strategy == "momentum":
                change=(vals[-1]-vals[-2])/vals[-2]
                if change > 0.002: decision="BUY"
                elif change < -0.002: decision="SELL"
            elif self.strategy == "mean_reversion":
                avg=sum(vals[-5:])/len(vals[-5:])
                deviation=(price-avg)/avg
                if deviation < -0.003: decision="BUY"
                elif deviation > 0.003: decision="SELL"
            elif self.strategy == "breakout":
                window=vals[-6:-1]
                if window:
                    if price > max(window): decision="BUY"
                    elif price < min(window): decision="SELL"
        record={"symbol":symbol,"price":price,"decision":decision,"strategy":self.strategy,"mode":"PAPER"}
        self.signals.append(record)
        if len(self.signals)>500: self.signals=self.signals[-500:]
        return record

class TraderArena:
    def __init__(self):
        self.profiles=[TraderProfile("Momentum","momentum"),TraderProfile("Mean Reversion","mean_reversion"),TraderProfile("Breakout","breakout")]
    def tick(self,symbol,price):
        return {"mode":"PAPER","live_orders_enabled":False,"symbol":symbol,"price":price,
                "traders":[{"name":p.name,"strategy":p.strategy,"virtual_capital":p.capital,"decision":p.evaluate(symbol,price)} for p in self.profiles]}
    def status(self):
        return [{"name":p.name,"strategy":p.strategy,"virtual_capital":p.capital,"signals":len(p.signals)} for p in self.profiles]
