import redis
import os

r = redis.Redis()

FAUCET_REQUEST_TIME_LIMIT = os.getenv('FAUCET_REQUEST_TIME_LIMIT') or 86400

def set_address(address:str):
    if r.get(address):
        return False
    r.mset({address: '1'})
    r.expire(address, FAUCET_REQUEST_TIME_LIMIT)
    return True