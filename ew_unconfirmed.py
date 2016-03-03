#!/usr/bin/python
import re
import time
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

# print data
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%( conf['rpcuser'] , conf['rpcpassword'] ) )
pattern=re.compile("4557(20|41|43)")
processed = []
while 1:
    starting = time.time()
    mempool = rpc_connection.getrawmempool()
    print "---------------------"
    print "mempool size: " + str(len(mempool))
    print "processed size: " + str(len(processed))
    toprocess = list( set(mempool) - set(processed) )
    print "toprocess size: " + str(len(toprocess))
    
    n = 20
    containEW = 0;
    toprocess_chunks = [toprocess[i:i+n] for i in range(0, len(toprocess) , n) ]

    ewtxs = []
    processed = []

    for i, chunk in enumerate(toprocess_chunks):
      print str(i) + "/" + str(len(toprocess_chunks));
      try:
        txs_data = rpc_connection.batch_( [ ["getrawtransaction", x] for x in chunk ] )
        for idx, tx_data in enumerate(txs_data):
          tx = chunk[idx];
          processed.append(tx)
          if pattern.search(tx_data):
            print "tx_data contains 4547(20|41|43)"
            containEW = containEW + 1
            decoded = rpc_connection.decoderawtransaction(tx_data)
            #todo verify OPRETURUN STARTS WITH 455720 455741 455743
            ewtxs.append(decoded)
      except:
        print "Unexpected error:", sys.exc_info()[0]
        

    print "elapsed: " + str(time.time() - starting)
    print "mempool size: " + str(len(mempool))
    print "processed size: " + str(len(processed))
    print "containEW: " + str(containEW)
    print "ewtxs: " + str(len(ewtxs)) + " of " + str(len(mempool) - already_done);

    if len(ewtxs)>0 and false :
        jsonresult = json.dumps(ewtxs, default=decimal_default)
        conn = httplib.HTTPConnection('eternitywall.it', 80)
        conn.connect()
        conn.request('POST', "/v1/hooks/ewunconfirmedtx" , jsonresult)
        resp = conn.getresponse()
        conn.close()
        print resp.status, resp.reason
    time.sleep(5)
