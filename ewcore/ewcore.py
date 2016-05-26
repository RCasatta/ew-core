import random
import http.client
import urllib

from ewcore.config import read_config_file
from mnemonic import Mnemonic
from pycoin.key.BIP32Node import BIP32Node
from bitcoin.wallet import CBitcoinSecret
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

EW_DERIVATION = 4544288


class EW(object):

    def __init__(self):
        conf = read_config_file("ew.conf")
        mnemo = Mnemonic('english')
        entropy = mnemo.to_entropy(conf['passphrase'])
        print("entropy=" + entropy.hex())
        master = BIP32Node.from_master_secret(entropy, 'BTC')
        print("master address=" + master.address())
        # /m/4544288'/0'/0'/0/0  alias
        alias = master.subkey(i=EW_DERIVATION, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=False).subkey(i=0, is_hardened=False)
        self.address = alias.address()
        print("alias address=" + self.address)
        self.key = CBitcoinSecret(alias.wif())

    def sign(self, message):
        message = BitcoinMessage(message)
        signature = SignMessage(self.key, message).decode('ascii')
        print("Address: %s" % self.key)
        print("Message: %s" % message)
        print("Signature: %s" % signature)
        assert VerifyMessage(self.address, message, signature)

        return signature

    def post_hash(self, hashvalue):
        return self.hash(hashvalue, 'POST')

    def get_hash(self, hashvalue):
        return self.hash(hashvalue, 'GET')

    def hash(self, hashvalue, method):
        challenge = str(random.random()) + hashvalue
        signature = self.sign(challenge)

        # http://eternitywall.it/v1/auth/hash/[hash]?account=[account]&signature=[signature]&challenge=[challenge]
        # for https use https://eternitywall.appspot.com/v1/auth/hash/[hash]?
        # account=[account]&signature=[signature]&challenge=[challenge]
        params = {'account': self.address, 'signature': signature, "challenge": challenge}
        print("params " + str(params))
        path = "/v1/auth/hash/" + hashvalue + "?" + urllib.parse.urlencode(params)

        # returns http code
        # 400 if bad missing unrecognized parameter
        # 401 if unauthorized (invalid signature or not existing account)
        # 200 if OK

        print(method + " path " + path)
        conn = http.client.HTTPConnection('eternitywall.it')
        conn.request(method, path)
        resp = conn.getresponse()
        print("resp " + str(resp.status) + "," + str(resp.reason))
        data = resp.read()
        conn.close()

        return data


