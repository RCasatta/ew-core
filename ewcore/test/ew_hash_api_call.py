#!/usr/bin/env python3

import hashlib

import random
import binascii

from ewcore import ewcore


def test_ew_call():
    # the following is the document we are hashing to commit in the blockchain, in this case a random string
    document = str(random.random())
    hash_value = binascii.hexlify(hashlib.sha256(document.encode()).digest()).decode('ascii')

    ew = ewcore.EW()
    ret_post = ew.post_hash(hash_value)

    print("ret_post=" + ret_post.decode())

    ret_get = ew.get_hash(hash_value)

    print("ret_get=" + ret_get.decode())


if __name__ == '__main__':
    test_ew_call()
