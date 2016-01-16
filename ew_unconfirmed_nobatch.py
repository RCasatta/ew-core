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

processed_file = '/tmp/processed_txs'

try:
  f = open(processed_file,'r')
  data = f.read() # python will convert \n to os.linesep
  f.close() # you can omit in most cases as the destructor will call it
except IOError:
  data = []

# print data
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%( conf['rpcuser'] , conf['rpcpassword'] ) )

mempool = rpc_connection.getrawmempool()
n = 10 # 100 rpc function call every request
ewtxs = []
for tx in mempool:
  if tx not in data:
    print tx
    txs_data = rpc_connection.getrawtransaction( tx )
    for idx, tx_data in enumerate(txs_data):
      if "455720" in tx_data:
        decoded = rpc_tion.decoderawtransaction(tx_data)
        ewtxs.append(decoded)

print "-------------"
print "mempool txs " + str(len(mempool))
print ewtxs;    

f = open(processed_file,'w')
f.write( json.dumps(mempool) ) # python will convert \n to os.linesep
f.close() # you can omit in most cases as the destructor will call it

if len(ewtxs)>0 :
  jsonresult = json.dumps(result, default=decimal_default)
  conn = httplib.HTTPConnection('eternitywall.it', 80)
  conn.connect()
  conn.request('POST', "/v1/hooks/ewunconfirmedtx" , jsonresult)
  resp = conn.getresponse()
  conn.close()
  print resp.status, resp.reason


 
