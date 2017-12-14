#!/usr/bin/env python3

import argparse
import hashlib
import binascii
from ewcore import ewcore

parser = argparse.ArgumentParser(
    description="Hash all files in a directory and push it to Eternity Wall",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('file', metavar='FILE', type=argparse.FileType('rb'),
                    help='Filename')


def sha256_fd(fd):
    hash_state = hashlib.sha256()
    chunk = True
    while chunk != b'':
        chunk = fd.read(2 ** 20)
        hash_state.update(chunk)

    return hash_state.digest()


def ew_file(file_to_stamp):
    # the following is the document we are hashing to commit in the blockchain, in this case a random string

    hash_bin = sha256_fd(file_to_stamp)
    hash_value = binascii.hexlify(hash_bin).decode('ascii')
    print("Hashing %s return %s " % (file_to_stamp.name, hash_value))

    ew = ewcore.EW()
    ret_post = ew.post_hash(hash_value)

    print("ret_post=" + ret_post.decode())

    ret_get = ew.get_hash(hash_value)

    print("ret_get=" + ret_get.decode())


if __name__ == '__main__':
    args=parser.parse_args()
    ew_file(args.file)
