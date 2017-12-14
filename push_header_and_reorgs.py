#!/usr/bin/env python3

import sys
import bitcoin.rpc
import binascii
import http.client
import json

block_hash_hex = sys.argv[1]
print(block_hash_hex)
block_hash_bytes = binascii.unhexlify(block_hash_hex)
block_hash_bytes_reversed = block_hash_bytes[::-1]

proxy=bitcoin.rpc.Proxy()

header = proxy.getblockheader(block_hash_bytes_reversed)
print(header)
headerHex = binascii.hexlify(header.serialize()).decode()
print(headerHex)

conn = http.client.HTTPSConnection("api.eternitywall.com")
conn.request("GET", "/authcal/v1/header/"+headerHex )

response = conn.getresponse()
print(str(response.status))
if response.status == 200:
    data = response.read()
    result = json.loads(data.decode('utf-8'))
    message = result['message']
    print(result)
    print(message)

    if message == "PreviousDoesNotExist":
        print("------------PreviousDoesNotExist----------")
        blockchaininfo=proxy._call("getblockchaininfo")
        myheight = blockchaininfo['headers']
        print(str(myheight))
        for i in range(myheight-10,myheight+1):
            hash = proxy.getblockhash(i)
            header = proxy.getblockheader(hash)
            headerHex = binascii.hexlify(header.serialize()).decode()
            print(str(i) + " " + str(binascii.hexlify(hash))  + " " + headerHex )
            conn = http.client.HTTPSConnection("api.eternitywall.com")
            conn.request("GET", "/authcal/v1/header/"+headerHex )
            response = conn.getresponse()
            data = response.read()
            print(str(response.status) + " " + str(response.reason) + " " + str(data))

