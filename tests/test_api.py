from fastapi.testclient import TestClient
from app.main import app, engine
from app.simulator import DemoEngine
client=TestClient(app)
def setup_function(): engine.stop(); engine.ledger.clear(); engine.last_price.clear()
def test_health(): assert client.get('/health').json()['mode']=='DEMO'
def test_pause_blocks_tick(): assert client.post('/paper/tick',json={'symbol':'BTCUSDT','price':100}).status_code==409
def test_start_tick_stop():
 client.post('/control/start'); r=client.post('/paper/tick',json={'symbol':'BTCUSDT','price':100}); assert r.status_code==200 and r.json()['live_order'] is False; client.post('/control/stop')
def test_config_saved():
 r=client.post('/config',json={'enabled':False,'daily_loss_limit':5,'trade_size':2}); assert r.status_code==200 and r.json()['live_orders_enabled'] is False
def test_persistence(tmp_path):
 e=DemoEngine(tmp_path/'persist.sqlite'); e.start(); e.tick('ETHUSDT',123); e.configure({'enabled':False,'daily_loss_limit':7,'trade_size':3}); restored=DemoEngine(tmp_path/'persist.sqlite'); assert restored.ledger[-1]['price']==123; assert restored.config['trade_size']==3

def test_trader_arena_api():
 client.post('/control/start')
 r=client.post('/paper/traders/tick',json={'symbol':'BTCUSDT','price':100})
 assert r.status_code==200 and len(r.json()['traders'])==3
 client.post('/control/stop')

def test_moderator_api_paper_only():
 client.post('/control/start')
 r=client.post('/paper/moderator/tick',json={'symbol':'BTCUSDT','price':100})
 assert r.status_code==200 and r.json()['live_orders_enabled'] is False
 client.post('/control/stop')
