#!/usr/bin/env python3

import decimal
import http.client
import json
import re
import sys
import time
import bitcoin.rpc
from datetime import datetime


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def ew_unconfirmed():
    """ask mempool to local bitcoin node, check for ew_transaction and send it to eternitywall.it"""

    rpc_connection = bitcoin.rpc.RawProxy()

    pattern = re.compile("4557(20|41|43)")
    processed = []

    # if it's not working --> https://github.com/jgarzik/python-bitcoinrpc/pull/58/files

    while 1:
        if 1:
            starting = time.time()
            mempool = rpc_connection.getrawmempool()
            print("---------------------")
            print("mempool size: " + str(len(mempool)))
            print("processed size: " + str(len(processed)))
            processed_set = set(processed)
            mempool_set = set(mempool)
            to_process = list(mempool_set - processed_set)
            print("to process size: " + str(len(to_process)))
            processed = list(mempool_set & processed_set)
            print("new processed size: " + str(len(processed)))
            contains_ew = 0
            ew_txs = []

            for tx in to_process:
                # print str(i) + "/" + str(len(to_process_chunks));
                try:
                    tx_data = rpc_connection.getrawtransaction(tx)
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

        # except Exception as e:
        #    print("Unexpected error2:", sys.exc_info()[0])
        #    print(e)
        time.sleep(5)


if __name__ == "__main__":
    ew_unconfirmed()