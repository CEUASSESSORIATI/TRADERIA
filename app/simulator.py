import json, logging, sqlite3
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR=Path('data'); DATA_DIR.mkdir(exist_ok=True)
DB=DATA_DIR/'engine.sqlite3'
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.FileHandler(DATA_DIR/'engine.log',encoding='utf-8'),logging.StreamHandler()])
log=logging.getLogger('ceu-engine')

class DemoEngine:
    def __init__(self, db_path=DB):
        self.db_path=Path(db_path); self.db_path.parent.mkdir(parents=True,exist_ok=True)
        self.running=False; self.config={'enabled':False,'daily_loss_limit':10.0,'trade_size':10.0}
        self.last_price={}; self.ledger=[]; self.strategies={'momentum':{},'mean_reversion':{},'breakout':{}}
        self._init_db(); self._restore()
    def _db(self): return sqlite3.connect(self.db_path)
    def _init_db(self):
        with self._db() as c:
            c.execute('CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY, timestamp TEXT, symbol TEXT, price REAL, decision TEXT, mode TEXT, live_order INTEGER)')
            c.execute('CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT)')
    def _restore(self):
        with self._db() as c:
            row=c.execute("SELECT value FROM state WHERE key='config'").fetchone()
            if row:
                try: self.config=json.loads(row[0])
                except (ValueError,TypeError): log.warning('Config state corrupt; using defaults')
            rows=c.execute('SELECT timestamp,symbol,price,decision,mode,live_order FROM ledger ORDER BY id DESC LIMIT 500').fetchall()
            self.ledger=[{'time':r[0],'symbol':r[1],'price':r[2],'decision':r[3],'mode':r[4],'live_order':bool(r[5])} for r in reversed(rows)]
            for _,sym,price,*_ in rows: self.last_price.setdefault(sym,price)
        log.info('State restored: %d ledger entries',len(self.ledger))
    def _save_config(self):
        with self._db() as c: c.execute("INSERT OR REPLACE INTO state(key,value) VALUES('config',?)",(json.dumps(self.config),))
    def configure(self,cfg): self.config=cfg; self._save_config(); log.info('Configuration updated')
    def start(self): self.running=True; log.info('Demo engine started')
    def stop(self): self.running=False; log.info('Demo engine paused')
    def status(self): return {'engine':'ready','running':self.running,'mode':'DEMO','live_orders_enabled':False,'config':self.config,'ledger_entries':len(self.ledger),'strategies':['momentum','mean_reversion','breakout']}
    def tick(self,symbol,price):
        prev=self.last_price.get(symbol); self.last_price[symbol]=price
        decision='observe' if prev is None else ('demo_signal_up' if price>prev else ('demo_signal_down' if price<prev else 'observe'))
        ts=datetime.now(timezone.utc).isoformat(); entry={'time':ts,'symbol':symbol,'price':price,'decision':decision,'mode':'DEMO','live_order':False}
        with self._db() as c: c.execute('INSERT INTO ledger(timestamp,symbol,price,decision,mode,live_order) VALUES(?,?,?,?,?,0)',(ts,symbol,price,decision,'DEMO'))
        self.ledger.append(entry); log.info('Simulated tick %s %.8f decision=%s',symbol,price,decision); return entry
