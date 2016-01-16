#!/usr/bin/python

import json
import sys
import httplib
import decimal
import config
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

conf = config.read_default_config();

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%( conf['rpcuser'] , conf['rpcpassword'] ) )

mempool = rpc_connection.getrawmempool()
n = 100 # 100 rpc function call every request
mempool_chunks = [mempool[i:i+n] for i in range(0, len(mempool) , n) ]
ewtxs = []
for chunk in mempool_chunks:
  txs_data = rpc_connection.batch_( [ ["getrawtransaction", x] for x in chunk ] )
  for idx, tx_data in enumerate(txs_data):
    if "455720" in tx_data:
      ewtxs.append( chunk[idx] )

print ewtxs;    

#jsonresult = json.dumps(result, default=decimal_default)
#print(jsonresult)

#conn = httplib.HTTPConnection('eternitywall.it', 80)
#conn.connect()
#conn.request('POST', "/v1/hooks/ewtx?hash=%s" % (block_hash) , jsonresult)
#resp = conn.getresponse()
#conn.close()
#print resp.status, resp.reason


 
