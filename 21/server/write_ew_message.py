#!/usr/bin/env python3
from flask import Flask, request

from two1.wallet.two1_wallet import Two1Wallet
from two1.blockchain.twentyone_provider import TwentyOneProvider
from two1.bitcoin import utils
from two1.bitcoin import Script
from two1.bitcoin import Transaction, TransactionInput, TransactionOutput
from two1.bitserv.flask import Payment

# Create application objects
app = Flask(__name__)
wallet = Two1Wallet(Two1Wallet.DEFAULT_WALLET_PATH, TwentyOneProvider())
payment = Payment(app, wallet)


@app.route('/write-ew-message')
@payment.required(1000)
def write_ew_message():
    """Write a message to the blockchain."""

    msg = request.args.get('message')

    # Create a bitcoin script object with our message
    if (len(msg) > 72):
        raise Exception('Message is too long and may not be accepted.')
    msg= "EW " + msg;
    message_script = Script('OP_RETURN 0x{}'.format(utils.bytes_to_str(msg.encode())))

    # Define the fee we're willing to pay for the tx
    tx_fee = 11000

    # Get the first UTXO from our set that can cover the fee
    utxo = None
    for utxo_addr, utxos in wallet.get_utxos().items():
        for u in utxos:
            if u.value > tx_fee:
                utxo = u
                break
        if utxo:
            break

    if not utxo:
        raise Exception('No UTXOs available to pay for the transaction.')

    # Build the transaction inputs (there is only one, but Transaction expects a list)
    inputs = [TransactionInput(outpoint=utxo.transaction_hash,
                               outpoint_index=utxo.outpoint_index,
                               script=utxo.script,
                               sequence_num=0xffffffff)]

    outputs = []
    # Build one output with our custom message script
    outputs.append(TransactionOutput(value=0, script=message_script))
    # Build another output to pay the UTXO money back to one of our addresses
    _, change_key_hash = utils.address_to_key_hash(wallet._accounts[0].get_next_address(True))
    outputs.append(TransactionOutput(value=utxo.value - tx_fee,
                                     script=Script.build_p2pkh(change_key_hash)))

    # Build an unsigned transaction object
    txn = Transaction(version=Transaction.DEFAULT_TRANSACTION_VERSION,
                      inputs=inputs,
                      outputs=outputs,
                      lock_time=0
                      )

    # Sign the transaction with the correct private key
    private_key = wallet.get_private_key(utxo_addr)
    txn.sign_input(input_index=0,
                   hash_type=Transaction.SIG_HASH_ALL,
                   private_key=private_key,
                   sub_script=utxo.script
                   )

    # Broadcast the transaction
    tx = wallet.broadcast_transaction(txn.to_hex())
    return tx

if __name__ == '__main__':
    app.run(host='0.0.0.0')
