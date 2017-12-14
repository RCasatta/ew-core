from mnemonic import Mnemonic
from pycoin.key.BIP32Node import BIP32Node
import binascii

EW_DERIVATION = 4544288

mnemo = Mnemonic('english')
entropy_from_pass = mnemo.to_entropy('your passphrase')
entropy_hex = binascii.hexlify(entropy_from_pass)
print(entropy_hex)  # save this in conf

######

entropy = binascii.unhexlify(entropy_hex)
master = BIP32Node.from_master_secret(entropy, 'BTC')
print("master address=" + master.address())

alias = master.subkey(i=EW_DERIVATION, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=True).subkey(i=0, is_hardened=False).subkey(i=0, is_hardened=False)
print("alias address=" + alias.address())

