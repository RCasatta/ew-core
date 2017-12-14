#!/usr/bin/env python3


from two1.wallet import Wallet
from two1.bitrequests import BitTransferRequests

wallet = Wallet()
requests = BitTransferRequests(wallet)

def post_hash(hash_value):
    print("post_hash('%s')" % hash_value)

    # 402 endpoint URL and request
    myurl = 'http://21.eternitywall.it/v1/hash?hash='+ hash_value
    resp = requests.post(myurl)

    print(resp.status_code)

# Read the text to speechify from the CLI
if __name__ == '__main__':
    import os
    import binascii
    import hashlib

    rand_string = os.urandom(32)
    hash_value = binascii.hexlify(hashlib.sha256(rand_string).digest()).decode('ascii')
    post_hash(hash_value)
