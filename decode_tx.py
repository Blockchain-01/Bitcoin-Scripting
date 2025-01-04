from bitcoin import SelectParams
from bitcoin.core import CTransaction, x

def decode_tx(hex_tx):
    # Select testnet network
    SelectParams('testnet')
    
    # Convert hex to bytes and decode
    tx = CTransaction.deserialize(x(hex_tx))
    
    # Print transaction details
    print("Transaction Details:")
    print(f"Version: {tx.nVersion}")
    print("\nInputs:")
    for tx_in in tx.vin:
        print(f"  Previous TX: {b2lx(tx_in.prevout.hash)}")
        print(f"  Output Index: {tx_in.prevout.n}")
        print(f"  ScriptSig: {b2x(tx_in.scriptSig)}")
        
    print("\nOutputs:")
    for tx_out in tx.vout:
        print(f"  Amount: {tx_out.nValue/COIN}")
        print(f"  ScriptPubKey: {b2x(tx_out.scriptPubKey)}")

if __name__ == "__main__":
    raw_tx = "00000000ac887a9dfb7dbda741be776874254da944df21581b13a976180000000000002710ac886e7c6e9c04a0cda79ab1866e1e09d1b6ebd85f13a9761800000000000026e902ffffffff98cff7f5de10e2571fe5ab3badd9fc01b100d332bc1f7e3233418d03b51c1e78032101b613c77fc29f92ff09c4d5c29277bfc5f158e20b7036e2a70bb580e416017c2f200202ef2b5f1003fa958b86fc086606ebb875579830abe819b46cac7952198f351220024430476a00000001fa979ca4e576399a5ac9c89dc42cc0faf487f51832c9fb5b0fca67d39083bed70100000001"
    decode_tx(raw_tx)