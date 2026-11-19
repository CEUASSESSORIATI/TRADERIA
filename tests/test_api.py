from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_demo():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['mode'] == 'DEMO'

def test_status_live_disabled():
    r = client.get('/status')
    assert r.status_code == 200
    assert r.json()['live_orders_enabled'] is False

def test_paper_tick():
    r = client.post('/paper/tick', json={'symbol':'BTCUSDT','price':50000})
    assert r.status_code == 200
    assert r.json()['live_order'] is False
