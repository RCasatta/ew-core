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
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % ( conf['rpcuser'], conf['rpcpassword']))

getinfo = rpc_connection.getinfo()
# print getinfo
# block_hash = rpc_connection.getbestblockhash()
# block_hash = "00000000000000000b664a85bce8dacc166bb9fcccad8ba3a644fb99407cf17c"
block_hash = sys.argv[1]
block = rpc_connection.getblock(block_hash)
# print block
result = {}
ewtxs = []
txs = block['tx']
result['hash']   = block_hash
result['height'] = block['height']
result['time']   = block['time']
for tx in txs:
   rawtx = rpc_connection.getrawtransaction(tx)
   if "4557" in rawtx:
      dectx = rpc_connection.decoderawtransaction(rawtx)
      ewtxs.append(dectx)

result['tx'] = ewtxs
jsonresult = json.dumps(result, default=decimal_default)
#print(jsonresult)

conn = httplib.HTTPConnection('eternitywall.it', 80)
conn.connect()
conn.request('POST', "/v1/hooks/ewtx?hash=%s" % (block_hash) , jsonresult)
resp = conn.getresponse()
conn.close()
print resp.status, resp.reason


 
