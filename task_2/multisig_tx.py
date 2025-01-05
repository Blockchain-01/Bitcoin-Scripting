import os
import requests
from bitcoin import *
from bitcoin.core import *
from bitcoin.core.script import *
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, P2SHBitcoinAddress

SelectParams('testnet')

def get_redeem_script(sender1_pubkey, sender2_pubkey):
  redeem_script = CScript([OP_2, sender1_pubkey, sender2_pubkey, OP_2, OP_CHECKMULTISIG])
  return redeem_script

def create_multisig(sender1_pubkey, sender2_pubkey):
  redeem_script = get_redeem_script(sender1_pubkey, sender2_pubkey)
  address = P2SHBitcoinAddress.from_redeemScript(redeem_script)
  return address


def create_txin(utxo_txid, utxo_index):
  txid = lx(utxo_txid)
  return CMutableTxIn(COutPoint(txid, utxo_index))

def create_txout(recipient_amount, recipient_addr, change_amount, change_addr, redeem_script):
  recipient_output = CMutableTxOut(recipient_amount*COIN, CScript(recipient_addr.to_scriptPubKey()))
  change_output = CMutableTxOut(change_amount*COIN, CScript([OP_HASH160, Hash160(redeem_script), OP_EQUAL]))

  return recipient_output, change_output

def create_signed_transaction(txin, txout, redeem_script, private_key_1, private_key_2):
  try:
    tx_inputs = [txin] if not isinstance(txin, list) else txin
    tx_outputs = [txout] if not isinstance(txout, list) else txout

    tx = CMutableTransaction(tx_inputs, tx_outputs)
    signHash = SignatureHash(redeem_script, tx, 0, SIGHASH_ALL)
    sig1 = private_key_1.sign(signHash) + bytes([SIGHASH_ALL])
    sig2 = private_key_2.sign(signHash) + bytes([SIGHASH_ALL])

    txin.scriptSig = CScript([OP_0, sig1, sig2, redeem_script])

    scriptPubKey = CScript([OP_HASH160, Hash160(redeem_script), OP_EQUAL])
    
    VerifyScript(txin.scriptSig, scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))
    return b2x(tx.serialize())
  except Exception as e:
    raise ValueError(e)


def broadcast_tx(tx_hex):
  url = "https://blockstream.info/testnet/api/tx"
  headers = {'Content-Type': 'text/plain'}
    
  try:
    response = requests.post(url, data=tx_hex, headers=headers)
    if response.status_code == 200:
      return response.text
    else:
      print(f"Response status: {response.status_code}")
      print(f"Response body: {response.text}")
      raise ValueError(f"Broadcasting failed: {response.text}")
  except Exception as e:
    raise ValueError(f"Error broadcasting transaction: {str(e)}")

def get_utxo_index_utxo_amount(utxo_txid, address_received):
    """Fetch transaction details and extract vin's vout index and value for a specified address."""
    url = f"https://blockstream.info/testnet/api/tx/{utxo_txid}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Extract "vout" index from "vin"
            vin_vout_index = data["vin"][0]["vout"]

            # Extract "value" from "vout" where "scriptpubkey_address" matches
            matching_value = None
            for vout in data["vout"]:
                if vout["scriptpubkey_address"] == address_received:
                    matching_value = vout["value"]
                    break

            # Return the extracted values
            return vin_vout_index, matching_value / COIN
        else:
            raise ValueError(f"Fetching transaction failed: {response.text}")
    except Exception as e:
        raise ValueError(f"Error fetching transaction details: {str(e)}")


def start(faucet_tx, sender_1, sender_2, recipient, multisig_address):
  try:
    utxo_txid = faucet_tx['utxo_txid']
    utxo_index, utxo_amount = get_utxo_index_utxo_amount(utxo_txid, multisig_address)
    txin = create_txin(utxo_txid, utxo_index)

    total_amount = 0.00027602
    recipient_amount = 0.0002
    change_amount = total_amount - recipient_amount - 0.00001

    redeem_script = get_redeem_script(sender_1['public_key'], sender_2['public_key'])

    recipient_output,change_output = create_txout(recipient_amount, recipient['address'], change_amount, multisig_address, redeem_script)
    txout = [recipient_output, change_output]

    raw_tx = create_signed_transaction(txin, txout, redeem_script, sender_1['private_key'], sender_2['private_key'])
    print(f"Raw Transaction: {raw_tx}")

    tx_hash = broadcast_tx(raw_tx)
    print(f"Transaction broadcasted! Hash: {tx_hash}")
    print(f"View transaction: https://blockstream.info/testnet/tx/{tx_hash}")

  except Exception as e:
    print(f"Error: {str(e)}")
