from bitcoin import SelectParams
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.core.key import CPubKey
import requests

def broadcast_transaction(tx_hex):
  try:
    response = requests.post(url, data=tx_hex, headers=headers)
    if response.status_code == 200:
      return response.text  
    else:
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

def get_transaction_info(txid):
  url = f"https://blockstream.info/testnet/api/tx/{txid}"
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
    else:
      raise ValueError(f"Failed to get transaction info: {response.text}")
  except Exception as e:
    raise ValueError(f"Error getting transaction info: {str(e)}")


def spend_locked_funds(sender_priv_key, utxo_txid, utxo_index, utxo_amount, recipient_addr, send_amount, change_address):
    try:
        SelectParams('testnet')

        utxo_amount_sats = int(utxo_amount * COIN)
        send_amount_sats = int(send_amount * COIN)
        change_amount_sats = utxo_amount_sats - send_amount_sats - int(0.00001 * COIN)  # Include fee

        secret_key = CBitcoinSecret(sender_priv_key)
        sender_pub_key = CPubKey(secret_key.pub)
        sender_address = P2PKHBitcoinAddress.from_pubkey(sender_pub_key)

        
        txid = lx(utxo_txid)
        outpoint = COutPoint(txid, utxo_index)
        txin = CMutableTxIn(outpoint)

        recipient_output = CMutableTxOut(send_amount_sats, P2PKHBitcoinAddress(recipient_addr).to_scriptPubKey())
        change_output = CMutableTxOut(change_amount_sats, P2PKHBitcoinAddress(change_address).to_scriptPubKey())

        tx = CMutableTransaction([txin], [recipient_output, change_output])

        sighash = SignatureHash(sender_address.to_scriptPubKey(), tx, 0, SIGHASH_ALL)
        sig = secret_key.sign(sighash) + bytes([SIGHASH_ALL])
        txin.scriptSig = CScript([sig, sender_pub_key])

        VerifyScript(txin.scriptSig, sender_address.to_scriptPubKey(), tx, 0, (SCRIPT_VERIFY_P2SH,))

        return b2x(tx.serialize())

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    sender_priv_key = "cU13K2WaezJtM65mPNBVvMr84QzLUANJcbZuT5yqmCeVMxqm4QNa"
    utxo_txid = "95f0a4ac7fe1b7446b1d165c4ae732803bdbc518d0b1d99badbb928a44d61c14"
    recipient_addr = "mkT3YKrMPgchhMy1AVyVvhQbYtFcwr9uJ7"
    change_address = "moaEaXS2d3ZoPVDWL9vwtMZxL7gURMHJwy"
    # utxo_index = 0
    # utxo_amount = 0.0001
    utxo_index, utxo_amount = get_utxo_index_utxo_amount(utxo_txid, change_address)
    send_amount = 0.00005
    try:
        raw_tx = spend_locked_funds(sender_priv_key, utxo_txid, utxo_index, utxo_amount, recipient_addr, send_amount, change_address)
        print(f"Raw Transaction: {raw_tx}")

        tx_hash = broadcast_transaction(raw_tx)
        print(f"Transaction broadcasted! Hash: {tx_hash}")
        print(f"View transaction: https://blockstream.info/testnet/tx/{tx_hash}")
        
        tx_info = get_transaction_info(tx_hash)
        print(f"Transaction details: {tx_info}")
        
    except Exception as e:
        print(f"Error: {str(e)}")