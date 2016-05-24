#!/usr/bin/env python3

import decimal
import http.client
import json
import re
import sys
import time
import bitcoinrpc
from datetime import datetime


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def ew_unconfirmed():
    """ask mempool to local bitcoin node, check for ew_transaction and send it to eternitywall.it"""

    rpc_connection = bitcoinrpc.connect_to_local()
    pattern = re.compile("4557(20|41|43)")
    processed = []

    # if it's not working --> https://github.com/jgarzik/python-bitcoinrpc/pull/58/files

    while 1:
        try:
            starting = time.time()
            mempool = rpc_connection.getrawmempool()
            print("---------------------")
            print("mempool size: " + str(len(mempool)))
            print("processed size: " + str(len(processed)))
            processed_set = set(processed)
            mempool_set = set(mempool)
            to_process = list( mempool_set - processed_set )
            print("to process size: " + str(len(to_process)))
            processed = list( mempool_set & processed_set )
            print("new processed size: " + str(len(processed)))
            n = 20
            contains_ew = 0;
            to_process_chunks = [to_process[i:i+n] for i in range(0, len(to_process), n)]
            ew_txs = []

            for i, chunk in enumerate(to_process_chunks):
                # print str(i) + "/" + str(len(to_process_chunks));
                try:
                    txs_data = rpc_connection.batch_([["getrawtransaction", x] for x in chunk])
                    for idx, tx_data in enumerate(txs_data):
                        tx = chunk[idx]
                        processed.append(tx)
                        if pattern.search(tx_data):
                            print("tx_data contains 4547(20|41|43)")
                            contains_ew += 1
                            decoded = rpc_connection.decoderawtransaction(tx_data)
                            # TODO verify OPRETURUN STARTS WITH 455720 455741 455743
                            ew_txs.append(decoded)
                except Exception as e:
                    print("Unexpected error1:", sys.exc_info()[0])
                    print(e)

            print("elapsed: " + str(time.time() - starting))
            print("contains_ew: " + str(contains_ew))
            print("now:" + str(datetime.now()))

            if len(ew_txs) > 0:
                print("posting on EW")
                json_result = json.dumps(ew_txs, default=decimal_default)
                conn = http.client.HTTPConnection('eternitywall.it', 80)
                conn.connect()
                conn.request('POST', "/v1/hooks/ewunconfirmedtx", json_result)
                resp = conn.getresponse()
                conn.close()
                print(resp.status, resp.reason)

        except Exception as e:
            print("Unexpected error2:", sys.exc_info()[0])
            print(e)
        time.sleep(5)
