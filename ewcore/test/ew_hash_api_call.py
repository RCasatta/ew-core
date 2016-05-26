#!/usr/bin/env python3

import hashlib
import http.client
import random
import urllib
import binascii

from ewcore.config import read_config_file
from mnemonic import Mnemonic
from bitcoin.wallet import CBitcoinSecret
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage
from pycoin.key.BIP32Node import BIP32Node

EW_DERIVATION = 4544288


def test_ew_call():
    # passphrase of an Eternity Wall account with a defined alias (you could use Eternity Wall android app
    # to obtain one or create by your own with the same rules)
    conf = read_config_file("ew.conf")

    mnemo = Mnemonic('english')
    entropy = mnemo.to_entropy(conf['passphrase'])
    print("entropy=" + entropy.hex())
    master = BIP32Node.from_master_secret(entropy, 'BTC')
    print("address=" + master.address())
    # /m/4544288'/0'/0'/0/0  alias
    alias = master.subkey(i=EW_DERIVATION, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=False).subkey(i=0, is_hardened=False)
    address = alias.address()
    print("alias=" + address)

    key = CBitcoinSecret(alias.wif())
    message = str(random.random())
    message = BitcoinMessage(message)
    signature = SignMessage(key, message).decode('ascii')

    assert VerifyMessage(address, message, signature)

    # the following is the document we are hashing to commit in the blockchain, in this case a random string
    document = str(random.random())
    hashvalue = binascii.hexlify(hashlib.sha256(document.encode()).digest()).decode('ascii')

    print("Address: %s" % address)
    print("Message: %s" % message)
    print("Signature: %s" % signature)
    print("Hashvalue: %s" % hashvalue)

    # http://eternitywall.it/v1/auth/hash/[hash]?account=[account]&signature=[signature]&challenge=[challenge]
    # for https use https://eternitywall.appspot.com/v1/auth/hash/[hash]?
    # account=[account]&signature=[signature]&challenge=[challenge]
    params = {'account': address, 'signature': signature, "challenge": message}
    url = "http://eternitywall.it/v1/auth/hash/" + hashvalue + "?" + urllib.parse.urlencode(params)

    # returns http code
    # 400 if bad missing unrecognized parameter
    # 401 if unauthorized (invalid signature or not existing account)
    # 200 if OK

    print("url=" + url)
    conn = http.client.HTTPConnection('eternitywall.it', 80)
    conn.connect()
    conn.request('POST', url, "")
    resp = conn.getresponse()
    conn.close()
    print("resp " + str(resp.status) + "," + str(resp.reason))

if __name__ == '__main__':
    test_ew_call()
