#!/usr/bin/env python3
import sys
import urllib.parse

from two1.wallet import Wallet
from two1.bitrequests import BitTransferRequests

wallet = Wallet()


def write_message(raw_msg):
    msg = urllib.parse.quote_plus(raw_msg)
    requests = BitTransferRequests(wallet)

    # purchase the bitcoin payable endpoint
    response = requests.get('http://localhost:5000/write-ew-message?message={}'.format(msg))

    # print out the transaction
    print("Transaction: {}".format(response.text))
    print("View it live at http://eternitywall.it/m/{}".format(response.text))

if __name__ == '__main__':
    write_message(sys.argv[1])
