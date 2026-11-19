from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .simulator import DemoEngine
app=FastAPI(title='CEU Trader Intelligence Engine',version='0.3.0',description='Demo simulation; no live orders.')
engine=DemoEngine()
class Tick(BaseModel): symbol:str=Field(default='BTCUSDT',min_length=3,max_length=20); price:float=Field(gt=0)
class Config(BaseModel): enabled:bool=False; daily_loss_limit:float=Field(default=10.0,gt=0); trade_size:float=Field(default=10.0,gt=0)
@app.get('/health')
def health(): return {'ok':True,'mode':'DEMO'}
@app.get('/status')
def status(): return engine.status()
@app.post('/config')
def set_config(config:Config): engine.configure(config.model_dump()); return engine.status()
@app.post('/control/start')
def start(): engine.start(); return engine.status()
@app.post('/control/stop')
def stop(): engine.stop(); return engine.status()
@app.post('/paper/tick')
def tick(req:Tick):
 if not engine.running: raise HTTPException(409,'Engine paused; start DEMO engine first')
 return engine.tick(req.symbol.upper(),req.price)
@app.get('/paper/ledger')
def ledger(): return engine.ledger
