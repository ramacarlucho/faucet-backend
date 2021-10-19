import uvicorn
import requests
import json
import os
from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel

from evmoswallet.converter import eth_to_evmos, evmos_to_eth
from evmosgrpc.messages.msgsend import create_msg_send
from evmosgrpc.builder import TransactionBuilder
from evmosgrpc.transaction import Transaction
from google.protobuf.json_format import MessageToDict

from fastapi.middleware.cors import CORSMiddleware

import db

SEED = os.getenv('EVMOS_FAUCET_SEED')

# Rama test key  = 6LcTwtocAAAAAJY2ef59GVG2w6xK2T5Ji6i333sW
RECAPTCHA_SECRET = os.getenv('RECAPTCHA_SECRET')

# Config
ALLOWED_HOSTS = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Address(BaseModel):
    address: str

class FaucetResponse(BaseModel):
    transactionHash : Optional[str]
    error: str

def authorize_recaptcha(token):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret':RECAPTCHA_SECRET, 'response':token})
    if response.ok:
        captchaResponse = json.loads(response.text)
        return captchaResponse['success']
    return False

def request_faucet(address):
    builder = TransactionBuilder(SEED)
    print (address)
    msg = create_msg_send(builder.address, address, 100)
    res = builder.send_tx(Transaction().generate_tx(builder, msg))
    dictResponse = MessageToDict(res)
    if 'code' in dictResponse['txResponse'].keys():
        return None, dictResponse['txResponse']['rawLog']
    return dictResponse['txResponse']['txhash'], ""

def verify_address(address):
    # TODO FIX ISSUE
    if address.startswith('evmos'):
        return eth_to_evmos(evmos_to_eth(address)) == address
    if address.startswith('0x'):
        return evmos_to_eth(eth_to_evmos(address)) == address
    return False


@app.post("/faucet/", response_model=FaucetResponse)
def faucet(address: Address, Authorization: str = Header(None)):
    canRequest = db.set_address(address.address)
    authorized = authorize_recaptcha(Authorization)
    if canRequest and authorized:
        txhash, err = request_faucet(address.address)
        return {'transactionHash': txhash, 'error':err}
    return {'transactionHash': None, 'error':"Not Authorized"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")