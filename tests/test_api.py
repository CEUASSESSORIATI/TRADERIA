from fastapi.testclient import TestClient
from app.main import app, engine
client = TestClient(app)

def setup_function():
    engine.stop(); engine.ledger.clear(); engine.last_price.clear()

def test_health():
    assert client.get('/health').json()['mode'] == 'DEMO'

def test_pause_blocks_tick():
    r=client.post('/paper/tick',json={'symbol':'BTCUSDT','price':100})
    assert r.status_code == 409

def test_start_tick_stop():
    client.post('/control/start')
    r=client.post('/paper/tick',json={'symbol':'BTCUSDT','price':100})
    assert r.status_code == 200 and r.json()['live_order'] is False
    client.post('/control/stop')

def test_config_risk_positive():
    r=client.post('/config',json={'enabled':False,'daily_loss_limit':5,'trade_size':2})
    assert r.status_code == 200
    assert r.json()['live_orders_enabled'] is False
