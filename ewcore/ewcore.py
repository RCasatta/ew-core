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

