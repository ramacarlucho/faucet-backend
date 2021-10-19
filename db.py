import redis
r = redis.Redis()

def set_address(address:str):
    if r.get(address):
        return False
    r.mset({address: '1'})
    r.expire(address, 30)
    return True