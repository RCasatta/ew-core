#!/usr/bin/env python3

import hashlib
import http.client
import random
import urllib
import binascii

from ewcore import ewcore

EW_DERIVATION = 4544288


def test_ew_call():
    # the following is the document we are hashing to commit in the blockchain, in this case a random string
    document = str(random.random())
    hashvalue = binascii.hexlify(hashlib.sha256(document.encode()).digest()).decode('ascii')
    challenge = str(random.random())

    ew = ewcore.EW()
    signature = ew.sign(challenge)

    # http://eternitywall.it/v1/auth/hash/[hash]?account=[account]&signature=[signature]&challenge=[challenge]
    # for https use https://eternitywall.appspot.com/v1/auth/hash/[hash]?
    # account=[account]&signature=[signature]&challenge=[challenge]
    params = {'account': ew.address, 'signature': signature, "challenge": challenge}
    print("params " + str(params))
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
