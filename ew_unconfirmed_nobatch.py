#!/usr/bin/python

import json
import sys
import httplib
import decimal
import config
import time
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

conf = config.read_default_config();

processed = []

# print data
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%( conf['rpcuser'] , conf['rpcpassword'] ) )


while 1:
  starting = time.time()
  mempool = rpc_connection.getrawmempool()
  n = 10 # 100 rpc function call every request
  already_done = 0
  doing = 0
  ewtxs = []
  for tx in mempool:
    if tx in processed:
      already_done = already_done + 1
    else: 
      tx_data = rpc_connection.getrawtransaction( tx )
      # print tx + ":" + tx_data
      if "455720" in tx_data:
        decoded = rpc_connection.decoderawtransaction(tx_data)
        ewtxs.append(decoded)

  print "---------------------"
  print "elapsed: " + str(time.time() - starting)
  print "mempool txs: " + str(len(mempool))
  print "already done: " + str(already_done)
  print "ewtxs: " + str(len(ewtxs)) + " of " + str(len(mempool) - already_done);
  processed = mempool   

  if len(ewtxs)>0 : 
    jsonresult = json.dumps(ewtxs, default=decimal_default)
    conn = httplib.HTTPConnection('eternitywall.it', 80)
    conn.connect()
    conn.request('POST', "/v1/hooks/ewunconfirmedtx" , jsonresult)
    resp = conn.getresponse()
    conn.close()
    print resp.status, resp.reason


 
