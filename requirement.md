# 1 Introduction

#In this task, we will start by explaining the fundamental structure of Bitcoin transactions and how

# scripts are used to lock and unlock funds.

# 2. Task

# Your first task is to create a simple Bitcoin script that locks funds to a specific address using the

# Pay-to-Public-Key-Hash (P2PKH) script. You will be provided with a testnet address.

# 3. Requirements

# Create a P2PKH Script: In Python, you can create a P2PKH script as follows:

```
# P2PKH Script

from bitcoin import *

from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

# Generate a random private key

private_key = CBitcoinSecret.from_secret_bytes(os.urandom(32))

# Derive the public key and Bitcoin address

public_key = private_key.pub

address = P2PKHBitcoinAddress.from_pubkey(public_key)

print("Private Key:", private_key)

print("Public Key:", public_key.hex())

print("Bitcoin Address:", address)
```

# Lock Funds: Use a Bitcoin testnet faucet to send testnet BTC to the generated Bitcoin address.

# • Spend Locked Funds: Write a Python script to spend the locked funds:

```
# Spend Locked Funds

from bitcoin import *

from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

# Private key and Bitcoin address from the previous step

private_key = CBitcoinSecret.from_secret_bytes(...)

address = P2PKHBitcoinAddress.from_pubkey(...)

# Create a transaction input (UTXO)

txid = "..." # Transaction ID of the UTXO you want to spend

output_index = ... # Index of the output in the transaction

txin = create_txin(txid, output_index)

# Create a transaction output to the desired destination

destination_address = "..." # Recipient’s address

amount_to_send = ... # Amount to send in satoshis

txout = create_txout(amount_to_send, destination_address)

# Create the transaction

tx = create_signed_transaction([txin], [txout], [private_key])

# Broadcast the transaction

broadcast_tx(tx)
```
