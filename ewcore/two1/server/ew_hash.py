import random
import hashlib
import binascii
from ewcore import ewcore

ew = ewcore.EW()


def ew_get_hash(hash):
    """get a hash stamp through ew."""
    print("ew_get_hash('%s')" % hash)
    return ew.get_hash(hash)


def ew_post_hash(hash):
    """Write a hash to the blockchain through ew."""
    print("ew_post_hash('%s')" % hash)
    return ew.post_hash(hash)


def is_hash(s):
    try:
        return int(s, 16) >= 0 and len(s) == 64
    except ValueError:
        return False


if __name__ == "__main__":
    document = str(random.random())
    hash_value = binascii.hexlify(hashlib.sha256(document.encode()).digest()).decode('ascii')
    print(ew_post_hash(hash_value))
    print(ew_get_hash(hash_value))
    print(is_hash('d4465232e3340f113202d589d20fd7e8bb3e743bca437cd46cda61df40789124'))

