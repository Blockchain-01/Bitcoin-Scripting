from bitcoin import SelectParams
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import b2x, b2lx, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.core.key import CPubKey
import requests

def broadcast_transaction(tx_hex):
  """Broadcast transaction to testnet using Blockstream API"""
  url = "https://blockstream.info/testnet/api/tx"
  headers = {'Content-Type': 'text/plain'}
    
  try:
    # Send raw hex as plain text in body
    response = requests.post(url, data=tx_hex, headers=headers)
    if response.status_code == 200:
      return response.text
    else:
      print(f"Response status: {response.status_code}")
      print(f"Response body: {response.text}")
      raise ValueError(f"Broadcasting failed: {response.text}")
  except Exception as e:
    raise ValueError(f"Error broadcasting transaction: {str(e)}")

  """Broadcast transaction to testnet using Blockstream API"""
  url = "https://blockstream.info/testnet/api/tx"
  headers = {'Content-Type': 'text/plain'}
  
  try:
    response = requests.post(url, data=tx_hex, headers=headers)
    if response.status_code == 200:
      return response.text  # Returns txid if successful
    else:
      # println(f"Broadcasting failed: {response.text}")
      raise ValueError(f"Broadcasting failed: {response.text}")
  except Exception as e:
    raise ValueError(f"Error broadcasting transaction: {str(e)}")

def get_transaction_info(txid):
  """Get transaction information from Blockstream API"""
  url = f"https://blockstream.info/testnet/api/tx/{txid}"
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
    else:
      raise ValueError(f"Failed to get transaction info: {response.text}")
  except Exception as e:
    raise ValueError(f"Error getting transaction info: {str(e)}")

def spend_locked_funds(priv_key_wif, utxo_txid, utxo_index, utxo_amount, recipient_address, send_amount, change_address=None):
  # Select testnet parameters
  SelectParams('testnet')
  
  # Validate inputs
  if not all([priv_key_wif, utxo_txid, recipient_address]):
    raise ValueError("Missing required parameters")
  
  # Create key objects
  secret = CBitcoinSecret(priv_key_wif)
  pub_key = secret.pub
  from_address = P2PKHBitcoinAddress.from_pubkey(pub_key)
  
  # Convert amounts to satoshis
  send_amount_satoshis = int(send_amount * COIN)
  feeBTC = 0.0001
  fee = int(feeBTC * COIN)  # 0.0001 BTC
  

  # Verify sufficient funds
  if utxo_amount < (send_amount + feeBTC):
    raise ValueError(f"Insufficient funds: {utxo_amount} < {send_amount + feeBTC}")
  
  # Create transaction input
  txin = CMutableTxIn(COutPoint(lx(utxo_txid), utxo_index))
  
  # Create outputs list
  outputs = []
  
  # Add recipient output
  recipient_addr_obj = P2PKHBitcoinAddress(recipient_address) 
  recipient_script = CScript([OP_DUP, OP_HASH160, recipient_addr_obj.to_bytes()[1:21], OP_EQUALVERIFY, OP_CHECKSIG])
  outputs.append(CMutableTxOut(send_amount_satoshis, recipient_script))
  
  # Add change output if needed
  change_amount = int((utxo_amount - send_amount - 0.00000001) * COIN)
  if change_amount >= 0 and change_address:
    change_addr_obj = P2PKHBitcoinAddress(change_address)
    change_script = CScript([OP_DUP, OP_HASH160, change_addr_obj.to_bytes()[1:21], OP_EQUALVERIFY, OP_CHECKSIG])
    outputs.append(CMutableTxOut(change_amount, change_script))
  
  # Create and sign transaction
  tx = CMutableTransaction([txin], outputs)
  sighash = SignatureHash(from_address.to_scriptPubKey(), tx, 0, SIGHASH_ALL)
  sig = secret.sign(sighash) + bytes([SIGHASH_ALL])
  txin.scriptSig = CScript([sig, pub_key])
  
  # Verify and return
  VerifyScript(txin.scriptSig, from_address.to_scriptPubKey(), tx, 0, (SCRIPT_VERIFY_P2SH,))
  return b2lx(tx.serialize())


# def spend_locked_funds(priv_key_wif, utxo_txid, utxo_index, utxo_amount, recipient_address, send_amount, change_address=None):
#     SelectParams('testnet')
    
#     # Key setup
#     secret = CBitcoinSecret(priv_key_wif)
#     pub_key = secret.pub
#     from_address = P2PKHBitcoinAddress.from_pubkey(pub_key)
    
#     # ------Amount (in satoshis)
#     utxo_amount_satoshis = int(utxo_amount * COIN)
#     send_amount_satoshis = int(send_amount * COIN)
#     fee = 1000 
    
#     # ----Validate amounts
#     if utxo_amount_satoshis < (send_amount_satoshis + fee):
#         raise ValueError(f"Insufficient funds: {utxo_amount_satoshis} < {send_amount_satoshis + fee}")
    
#     # -Create input
#     txin = CMutableTxIn(
#         COutPoint(lx(utxo_txid), utxo_index),
#         nSequence=0xffffffff
#     )
    
#     # ---Create outputs
#     outputs = []
    
#     # ---Recipient output
#     outputs.append(CMutableTxOut(
#         send_amount_satoshis,
#         P2PKHBitcoinAddress(recipient_address).to_scriptPubKey()
#     ))

    
#     # ----Change output
#     change_amount = utxo_amount_satoshis - send_amount_satoshis - fee
#     if change_amount >= 546 and change_address:
#         outputs.append(CMutableTxOut(
#             change_amount,
#             P2PKHBitcoinAddress(change_address).to_scriptPubKey()
#         ))
    
#     # ----Create transaction
#     tx = CMutableTransaction(
#         vin=[txin],
#         vout=outputs,
#         nVersion=2,
#         nLockTime=0
#     )
    
#     # !!!!! Sign transaction 
#     scriptPubKey = from_address.to_scriptPubKey()
#     sighash = SignatureHash(scriptPubKey, tx, 0, SIGHASH_ALL)
#     sig = secret.sign(sighash) + bytes([SIGHASH_ALL])
#     txin.scriptSig = CScript([sig, pub_key])
    
    
#     try:# Verify
#         VerifyScript(txin.scriptSig, scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))
#         print("Local verification passed")
#     except Exception as e:
#         print(f"Verification failed: {str(e)}")
#         raise
    
#     return b2lx(tx.serialize())


# Example usage
if __name__ == "__main__":
  # Transaction details
  sender_priv_key = "cPf6iq9Uo6Qq1PretmAWmAzj3SyeA4ZAEx5n6ME7eKhguV6N7Af7"
  utxo_txid = "fa979ca4e576399a5ac9c89dc42cc0faf487f51832c9fb5b0fca67d39083bed7"
  utxo_index = 1
  utxo_amount = 0.00019962
  recipient_addr = "moaEaXS2d3ZoPVDWL9vwtMZxL7gURMHJwy"
  send_amount = 0.00009961
  change_address = "mkT3YKrMPgchhMy1AVyVvhQbYtFcwr9uJ7"

  try:
    tx_hex = spend_locked_funds(
      sender_priv_key,
      utxo_txid,
      utxo_index,
      utxo_amount,
      recipient_addr,
      send_amount,
      change_address
    )
    print(f"Transaction hex: {tx_hex}")
    
    # Broadcast using Blockstream API
    tx_hash = broadcast_transaction(tx_hex)
    print(f"Transaction broadcasted! Hash: {tx_hash}")
    print(f"View transaction: https://blockstream.info/testnet/tx/{tx_hash}")
    
    # Get transaction details
    tx_info = get_transaction_info(tx_hash)
    print(f"Transaction details: {tx_info}")
        
  except Exception as e:
    print(f"Error: {str(e)}")



# Private Key: cPf6iq9Uo6Qq1PretmAWmAzj3SyeA4ZAEx5n6ME7eKhguV6N7Af7
# Public Key: 03781e1cb5038d4133327e1fbc32d300b101fcd9ad3babe51f57e210def5f7cf98
# Bitcoin Address: mkT3YKrMPgchhMy1AVyVvhQbYtFcwr9uJ7


# Private Key: cU13K2WaezJtM65mPNBVvMr84QzLUANJcbZuT5yqmCeVMxqm4QNa
# Public Key: 02af35fb9ecd89fa081e6192182deecf48288efa3a9d2382ed3db7296924df7485
# Bitcoin Address: moaEaXS2d3ZoPVDWL9vwtMZxL7gURMHJwy

# First Run:
# Signed transaction: 00000000ac887a9dfb7dbda741be776874254da944df21581b13a976180000000000002710ac886e7c6e9c04a0cda79ab1866e1e09d1b6ebd85f13a9761800000000000026e902ffffffff98cff7f5de10e2571fe5ab3badd9fc01b100d332bc1f7e3233418d03b51c1e78032101b613c77fc29f92ff09c4d5c29277bfc5f158e20b7036e2a70bb580e416017c2f200202ef2b5f1003fa958b86fc086606ebb875579830abe819b46cac7952198f351220024430476a00000001fa979ca4e576399a5ac9c89dc42cc0faf487f51832c9fb5b0fca67d39083bed70100000001