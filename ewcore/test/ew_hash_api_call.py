#! /usr/bin/env python

import hashlib
import httplib
import random
import urllib

from mnemonic import Mnemonic
from pycoin.serialize import b2h
from signmessage import sign_and_verify

EW_DERIVATION = 4544288

def test_ew_derivation(self):
    code = 'this passphrase will not work'  # passphrase of an Eternity Wall account with a defined alias (you could use Eternity Wall android app to obtain one or create by your own with the same rules)
    mnemo = Mnemonic('english')
    entropy = mnemo.to_entropy(code)

    # /m/4544288'/0'/0'/0/0  alias
    alias = master.subkey(i=EW_DERIVATION, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=False).subkey(i=0, is_hardened=False)

    challenge = str(random.random())
    print "challenge= " + challenge

    hashvalue = b2h(hashlib.sha256(challenge).digest())
    print "hash= " + hashvalue

    compressed = True
    account = alias.bitcoin_address()
    signature = sign_and_verify(alias.wif() , challenge, account, compressed)
    print "signature:" + signature

    # http://eternitywall.it/v1/auth/hash/[hash]?account=[account]&signature=[signature]&challenge=[challenge]
    # for https use https://eternitywall.appspot.com/v1/auth/hash/[hash]?account=[account]&signature=[signature]&challenge=[challenge]
    params = { 'account' : account, 'signature' : signature, "challenge" : challenge }
    url = "http://eternitywall.it/v1/auth/hash/" + hashvalue + "?" + urllib.urlencode(params)

    # returns http code
    # 400 if bad missing unrecognized parameter
    # 401 if unauthorized (invalid signature or not existing account)
    # 200 if OK

    print url
    conn = httplib.HTTPConnection('eternitywall.it', 80)
    conn.connect()
    conn.request('POST', url , "")
    resp = conn.getresponse()
    conn.close()
    print resp.status, resp.reason

if __name__ == '__main__':
    unittest.main()
