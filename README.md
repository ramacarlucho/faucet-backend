## Guide

Set Environment variables

```
RECAPTCHA_SECRET = [RECAPTCHA_SECRET_KEY]
EVMOS_FAUCET_SEED = [FAUCET WALLET SEED]```
```

The backend needs a redis-server to check the 24hs request limit
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

