from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin import SelectParams

SelectParams('testnet')

def create_wallet(private_key):
  owner = {}
  owner['private_key'] = CBitcoinSecret(private_key)
  owner['public_key'] = owner['private_key'].pub
  owner['address'] = P2PKHBitcoinAddress.from_pubkey(owner['public_key'])
  return owner