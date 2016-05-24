#!/usr/bin/env python3

import hashlib
import binascii

# double sha256
h2=lambda x: hashlib.sha256(hashlib.sha256(x).digest()).digest()
# unhex
u=lambda x: binascii.unhexlify(x)
# hex
x=lambda x: binascii.hexlify(x)
# reverse (for binary only)
r=lambda x: x[::-1]

mytest = {
'tx':[ u(e) for e in [
"02f2024d091fe12fdc23156a31dc63888e1ff227986fad36019b54d1fb5512cd",
"1c28f7d48a1141487634faa8592cd74e9034ddb038f4d7d166470cf1e32e095d",
"3cfaeaf48099aeeb2a043a0bbcda5594b85d204c194672954684ddcfbd5e4a9d",
"4fa62e391e4740251390c6f8ca32be00faffcc0266e684756e45563655655cd8",
"6565a08c3d58e683fb49f7e1ae43d4c58d406d15e4f980d093dc427de46f728f",
"7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6",
"8813009526907254e49fe59f79fb678e92ab04d185295165cc1c2c14b11c3fba",
"8cdaa991aee8f5c9a5dbcfb907e0392a2a0f5bab29f6122e1417618be21d1605",
"8dc375b430a765cc0b3e2b2b3584d7a41b69d88802328a99861b6c7531331997",
"a722a4e19998925ffe9cf70b11a528a274b716af4fdb18fa3583bec3ebfb56ac",
"aaa93f86aa25a650c596f98e7006f6a090597263df6e116faa0e8fbdb9a36cc6",
"c71d7584e3848bc129095fd21f34c9357721b94b626db0378e5f819330f3b3aa",
"cca1e2ac443cb03dccd3ca7c8ce95b17a2794e4e035efa47fd9940139916e317",
"dc025077c1211901d4eb71205819f91c35c9bd23008563de967771dac265fcae",
"e75160776cab3b505c41ee9f5bfd8101bf73317a36cef35870d767fa33afc3ee",
"f790d0299a1cc4ae97cbf92f97c2f2fc6857e29c12dd406c321587c69de4cb09"]
],

"root":u(b"5306fa61bfd6e6ccceffe635db4d2d2a4d6d2422f7a45ec6f707ce23c4fce111")
}

# Power of 2 transaction test case (8 tx)
# https://blockchain.info/block/000000000000307b75c9b213f61b2a0c429a34b41b628daae9774cb9b5ff1059
block120210 = {
    # merkle root from blockchain.info is in big endian already (in raw block its in little endian)
    'root': u(b'0b0192e318af62f8f91243948ea4c7ea9d696197e88b9401bce35ecb0a0cb59b'),

    # transactions/leaves in big endian (regular) binary (some h2(TXDATA))
    'tx': [r(u(e)) for e in [
        # little endian TXIDs = (some x(r(h2(TXDATA)))) [byte-reversed hashes]
        # as shown on blockchain.info
        b'04a2808134e646ba67ff83f0bc7535a008b6e154c98953f5e2c9d40429880faf',
        b'b6b3ff7b4d004a788c751f3f8fc881f96c7b647ae06eb9a720bddc924e6f9147',
        b'e614ebb7e059e248e1f4c440f91af5c9617394a05d72233d7acf6feb153362f1',
        b'5bbc4545145126108c91689e62c1806646468c547999241f5c2883a526e015b6',
        b'de56c21783d3d466c0a5a155ed909c7011879df1996d8c418dac74465ebc3564',
        b'd327f96d32afdbf4238458684570189de26ba5dc300d5cd19fa1a9cdcecdb527',
        b'702c3d845810f31c194e7c9ea3d2b3636f3b8b9ee71f3d93a2f36e9d1a4e9a81',
        b'b320e44b0e4cbe5973b4ebdea0c63939f9cc196982e3f4d15daaa1baa16f0004',
    ]],
}

# Uneven test case (13 tx)
# https://blockchain.info/block/0000000000004563d49a8e7f7f2a2f0aec01101fa971fb63714b8fbf32f62f91
block120192 = {
    # merkle root from blockchain.info is in big endian already (in raw block its in little endian)
    'root': u(b'560a4d3b44e57ff78be70d29698a8f98ce11677c1a59fb9966a7cd1795c9b47b'),

    # transactions/leaves in big endian (regular) binary (some h2(TXDATA))
    'tx': [r(u(e)) for e in [
        # little endian TXIDs (some x(r(h2(TXDATA)))) [byte-reversed hashes]
        # as shown on blockchain.info
        b'df70f26b6df54332ad29c08aab5e5d5560d1468311e90484ebd89f87ac6264e8',
        b'2148314cd02237786abe127f23b7346df8a116a2851745cb987652a3e132fc50',
        b'06c303894833eb5d639f06f95ceb2c4bd08e0ab4ae1d94cccfa54f02e9b35990',
        b'90ae3d27a5215dbb8e2e1657c927f81bdb9601106a6159f5384b4cde53836f24',
        b'51cfe20029ed6366e7f475a123ad84c96c54522e9ae64cb2f548811124a6f833',
        b'1e856be000b0fbaa5929b887755095106f4f0d3d19f9cd9cb07ab2239c8b4b18',
        b'9d6314d68d9de8250513563e02f83ffc80973ec8b7c2966835e2cbcac3320898',
        b'5d6e3fc4b0c44b867b83b7d7ca365754a8bb87d93c4f365ecacc1f0109b4c99c',
        b'58afcfed0a60792c3e15d8bb2bd8d59f2a968639473e575e2fc1c270fcfae910',
        b'50a0e15c32c257934f75ee2fa125dd7e9a542d38b5989efc380ea2c06a299804',
        b'acd706cdbe74f82040cc583e42dfc28d8603c2f7d2fe29c0d41ee2e8d78be51b',
        b'c7be55d3b55bd59f1ca19d2dc3ffbe8c28917c9e27f02456872755215b4b8a1f',
        b'e323fe6719e707b8deb108d3f4bcc43d9e018cf48e027b8f88941886a0744f60',
    ]],
}

# reduces list of hashes (input handles binary NOT hex here)
def merkle_root(txs):
    nodelist = txs

    # merge list until one element remaining
    while len(nodelist) > 1:
        newnodelist = []
        for idx in range(0, len(nodelist), 2):
            # detemine the two hashes to merge
            if idx != len(nodelist)-1:
                # normally, an even index node and next (odd index) node
                nl, nr = nodelist[idx], nodelist[idx+1]
            else: # potential special case on end: odd node pairs with itself
                nl, nr = nodelist[idx], nodelist[idx]
            # SHA256(SHA256(left concat right))
            # note how there is no reversing here related to Bitcoins endianness before or after the hash
            newnodelist.append(h2(nl + nr))
        nodelist = newnodelist

    return nodelist[0]

def process_block(blk):
    croot = x(r(merkle_root(blk['tx'])))
    print('Calculated merkle root %s' % croot.decode(), end='')
    assert(croot == x(blk['root']))
    print(' (value correct)')

process_block(block120210)
process_block(block120192)
process_block(mytest)
