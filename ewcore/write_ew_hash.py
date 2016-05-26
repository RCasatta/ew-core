import random
import hashlib
import binascii





def write_ew_hash(hash):
    """Write a hash to the blockchain through ew."""
    print("write_ew_hash('%s')" % hash)
    write_ew_hash(key,hash)



if __name__ == "__main__":
    document = str(random.random())
    hashvalue = binascii.hexlify(hashlib.sha256(document.encode()).digest()).decode('ascii')
    write_ew_hash(hashvalue)