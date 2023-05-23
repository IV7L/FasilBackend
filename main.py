from web3 import Web3, HTTPProvider
from eth_account.messages import encode_defunct

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/3f8783d83dc14864a098005310eb73a5"))

message = encode_defunct(text="I'm signing for login using this nonce 377838")
signature='0x7c028099d61f54d1b0b86d49fd8f5f5631a5414e44136e70df0f1ab5c75210c246f533a0ca5c80b9ce1128060ca7fe57cd2c77e2681b6aab8e6dab7dc4dc62771c'
print(w3.eth.account.recover_message(message, signature=signature))
    
