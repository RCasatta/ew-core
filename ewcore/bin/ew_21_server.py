#!/usr/bin/env python3

import json
import flask
import yaml
import os

from flask import request, abort
from two1.bitserv.flask import Payment
from two1.wallet import Wallet
from ewcore.two1.server.ew_hash import ew_get_hash, ew_post_hash, is_hash
from ewcore.two1.server.write_ew_message import write_ew_message


app = flask.Flask(__name__)
payment = Payment(app, Wallet())


@app.route('/hello')
@payment.required(1000)
def hello():
    return 'Hello, world'


@app.route('/v1/message')
@payment.required(1000)
def write_ew_message_endpoint():
    print("write_ew_message_endpoint()")
    msg = request.args.get('message')
    write_ew_message(msg)
    return msg


@app.route('/v1/hash', methods=['GET'])
@payment.required(100)
def v1_hash_get():
    print("ew_get_hash()")
    hash_value = check_input()
    return ew_get_hash(hash_value)


@app.route('/v1/hash', methods=['POST'])
@payment.required(1000)
def v1_hash_post():
    print("ew_post_hash()")
    hash_value = check_input()
    return ew_post_hash(hash_value)


def check_input():
    hash_value = request.args.get('hash')
    print("hash_value=" + hash_value)
    if not is_hash(hash_value):
        print("hash not valid")
        abort(400)
    return hash_value


@app.route('/manifest')
def manifest():
    """Provide the app manifest to the two1 crawler."""
    a = os.path.dirname(os.path.abspath(__file__))
    with open('./manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)


@app.route('/client')
def client():
    """Provides an example client script."""

    return ""  # send_from_directory('static', 'client.py')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


