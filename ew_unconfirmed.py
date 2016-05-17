#!/usr/bin/python
import re
import time
import json
import sys
import httplib
import decimal
import config
from datetime import datetime
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

# if it's not working --> https://github.com/jgarzik/python-bitcoinrpc/pull/58/files

while 1:
    try:
        starting = time.time()
        mempool = rpc_connection.getrawmempool()
        print "---------------------"
        print "mempool size: " + str(len(mempool))
        print "processed size: " + str(len(processed))
        processed_set = set(processed)
        mempool_set   = set(mempool)
        toprocess = list( mempool_set - processed_set )
        print "toprocess size: " + str(len(toprocess))
        processed = list( mempool_set & processed_set )
        print "new processed size: " + str(len(processed))

        n = 20
        containEW = 0;
        toprocess_chunks = [toprocess[i:i+n] for i in range(0, len(toprocess) , n) ]

        ewtxs = []

        for i, chunk in enumerate(toprocess_chunks):
          # print str(i) + "/" + str(len(toprocess_chunks));
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
          except Exception,e:
            print "Unexpected error1:", sys.exc_info()[0]
            print e

        print "elapsed: " + str(time.time() - starting)
        print "containEW: " + str(containEW)
        print "now:" + str(datetime.now())

        if len(ewtxs)>0 :
            print "posting on EW"
            jsonresult = json.dumps(ewtxs, default=decimal_default)
            conn = httplib.HTTPConnection('eternitywall.it', 80)
            conn.connect()
            conn.request('POST', "/v1/hooks/ewunconfirmedtx" , jsonresult)
            resp = conn.getresponse()
            conn.close()
            print resp.status, resp.reason
        ewtxs=[]
    except Exception,e:
      print "Unexpected error2:", sys.exc_info()[0]
      print e;
    time.sleep(5)
