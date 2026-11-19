from datetime import datetime, timezone

class DemoEngine:
    def __init__(self):
        self.running = False
        self.config = {'enabled': False, 'daily_loss_limit': 10.0, 'trade_size': 10.0}
        self.ledger = []
        self.last_price = {}

    def configure(self, cfg):
        # Real execution is deliberately unavailable in this build.
        self.config = cfg

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def status(self):
        return {'engine': 'ready', 'running': self.running, 'mode': 'DEMO', 'live_orders_enabled': False, 'config': self.config, 'ledger_entries': len(self.ledger)}

    def tick(self, symbol, price):
        prev = self.last_price.get(symbol)
        decision = 'observe' if prev is None else ('demo_signal_up' if price > prev else ('demo_signal_down' if price < prev else 'observe'))
        self.last_price[symbol] = price
        entry = {'time': datetime.now(timezone.utc).isoformat(), 'symbol': symbol, 'price': price, 'decision': decision, 'mode': 'DEMO', 'live_order': False}
        self.ledger.append(entry)
        return entry
