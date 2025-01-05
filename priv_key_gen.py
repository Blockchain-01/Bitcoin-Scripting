from bitcoin import *
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import os

SelectParams('testnet')

# Generate a random private key
private_key = CBitcoinSecret.from_secret_bytes(os.urandom(32))

# Derive the public key and Bitcoin address
public_key = private_key.pub
address = P2PKHBitcoinAddress.from_pubkey(public_key)

print("Private Key:", private_key)
print("Public Key:", public_key.hex())
print("Bitcoin Address:", address)

# Get the WIF (Wallet Import Format) of the private key 

# Private Key: cPf6iq9Uo6Qq1PretmAWmAzj3SyeA4ZAEx5n6ME7eKhguV6N7Af7
# Public Key: 03781e1cb5038d4133327e1fbc32d300b101fcd9ad3babe51f57e210def5f7cf98
# Bitcoin Address: mkT3YKrMPgchhMy1AVyVvhQbYtFcwr9uJ7

# https://blockstream.info/testnet/tx/fa979ca4e576399a5ac9c89dc42cc0faf487f51832c9fb5b0fca67d39083bed7


# Private Key: cU13K2WaezJtM65mPNBVvMr84QzLUANJcbZuT5yqmCeVMxqm4QNa
# Public Key: 02af35fb9ecd89fa081e6192182deecf48288efa3a9d2382ed3db7296924df7485
# Bitcoin Address: moaEaXS2d3ZoPVDWL9vwtMZxL7gURMHJwy

