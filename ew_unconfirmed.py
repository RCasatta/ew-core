#!/usr/bin/python

import json
import sys
import httplib
import decimal
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

rpc_user = "xenoky"
rpc_password = "Sua39_0hKJhfgdr7ub39jrmp99278Gjgtyfgi75fk4eop3h_145by_s4dE"

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (rpc_user, rpc_password))

mempool = rpc_connection.getrawmempool()
print mempool
for curr in mempool:

   print curr


#for tx in txs:
#   rawtx = rpc_connection.getrawtransaction(tx)
#   if "455720" in rawtx:
#      dectx = rpc_connection.decoderawtransaction(rawtx)
#      ewtxs.append(dectx)

#result['tx'] = ewtxs
#jsonresult = json.dumps(result, default=decimal_default)
#print(jsonresult)

#conn = httplib.HTTPConnection('eternitywall.it', 80)
#conn.connect()
#conn.request('POST', "/v1/hooks/ewtx?hash=%s" % (block_hash) , jsonresult)
#resp = conn.getresponse()
#conn.close()
#print resp.status, resp.reason


 
