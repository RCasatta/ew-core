#!/usr/bin/env python3


import decimal
import http.client
import json
import sys
import bitcoinrpc


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def ew_exctract():
    rpc_connection = bitcoinrpc.connect_to_local()
    getinfo = rpc_connection.getinfo()
    print(getinfo)

    # block_hash = rpc_connection.getbestblockhash()
    # block_hash = "00000000000000000b664a85bce8dacc166bb9fcccad8ba3a644fb99407cf17c"
    block_hash = sys.argv[1]
    block = rpc_connection.getblock(block_hash)
    # print block
    result = {}
    ew_txs = []
    txs = block['tx']
    result['hash'] = block_hash
    result['height'] = block['height']
    result['time'] = block['time']
    for tx in txs:
        raw_tx = rpc_connection.getrawtransaction(tx)
        if "4557" in raw_tx:
            dectx = rpc_connection.decoderawtransaction(raw_tx)
            ew_txs.append(dectx)

    result['tx'] = ew_txs
    jsonresult = json.dumps(result, default=decimal_default)
    # print(jsonresult)

    conn = http.client.HTTPConnection('eternitywall.it', 80)
    conn.connect()
    conn.request('POST', "/v1/hooks/ewtx?hash=%s" % block_hash, jsonresult)
    resp = conn.getresponse()
    conn.close()
    print(resp.status, resp.reason)


 
