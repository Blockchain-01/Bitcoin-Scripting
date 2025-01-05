from multisig_tx import *
from utils import *

private_key_1 = "cRuZ374LfeoaE4AK8LquBEqDBTBNFZRqERvbhQigseX919jQtASv"
private_key_2 = "cNk2RhvqFY1aWAa8C5EcKDyZgpkZHYLZzF4WWVQPFRrJAPCKX6Gt"
private_key_recipient = "cU13K2WaezJtM65mPNBVvMr84QzLUANJcbZuT5yqmCeVMxqm4QNa"


sender_1 = create_wallet(private_key_1)
sender_2 = create_wallet(private_key_2)
recipient = create_wallet(private_key_recipient)

multisig_address = create_multisig(sender_1['public_key'], sender_2['public_key']) #2Mx8Grwu3wUki45fCH2NzgPxkjuV8a1JUn4
print("Multisig Address:", multisig_address)

faucet_tx ={
  'utxo_txid': "5f0fbf952c64464c0b5c5c4d06f571e66d3ce958ce99d4027ef9c52bbb5cfcab", 
  'utxo_index': 1,
}

start(faucet_tx, sender_1, sender_2, recipient, multisig_address)
