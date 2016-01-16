#!/usr/bin/python

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import config
import time

conf = config.read_default_config();

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%( conf['rpcuser'] , conf['rpcpassword'] ) )
best_block_hash = rpc_connection.getbestblockhash()
print(best_block_hash)

starttime = time.time()
start = 362372  # first block with EW messages
last  = 392173
n = 100
ewtxs = []
blocks = range(start, last)
block_chunks = [blocks[i:i+n] for i in range(0, last-start, n) ]
for iternow in block_chunks :
  startchunk = time.time()
  txs_in_chunk = 0
  ewtxs_num = 0
  #print(iternow)
  commands = [ [ "getblockhash", b] for b in iternow ]
  block_hashes = rpc_connection.batch_(commands)
  blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
  for block in blocks :
    txs = block['tx']
    txs_num = len(txs)
    txs_in_chunk = txs_in_chunk + txs_num;
    # print( "txs in block " + str(block['height']) + ":" + str(txs_num) )
    chunks = [txs[i:i+n] for i in range(0, txs_num, n) ]
    for chunk in chunks :
      txs_data = rpc_connection.batch_( [ ["getrawtransaction", x] for x in chunk ] )
      for tx_data in txs_data :
        if "455720" in tx_data:
          ewtxs.append(tx_data)
          ewtxs_num = ewtxs_num + 1
  endchunk = time.time() - startchunk
  print("start_block=" + str(iternow[0]) + " took " + str(endchunk) + "s there was " + str(txs_in_chunk) + " of which of ew " + str(ewtxs_num) )

print( "tx found: " + str(len(ewtxs))  )
