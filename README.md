## Guide

Set Environment variables

```

RECAPTCHA_SECRET = [RECAPTCHA_SECRET_KEY]
EVMOS_FAUCET_SEED = [FAUCET WALLET SEED]```

[OPTIONAL]
FAUCET_REQUEST_TIME_LIMIT = [TIME BETWEEN REQUESTS IN SECONDS | DEFAULT 86400] 
```

The backend needs a redis-server to check the time request limit
```
redis-server
```

Create virtual env and run
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python api.py
```

