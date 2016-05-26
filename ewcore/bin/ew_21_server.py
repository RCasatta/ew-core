import json

import flask
import yaml
from flask import request
from two1.bitserv.flask import Payment
from two1.wallet import Wallet

from ewcore.two1.server.write_ew_message import write_ew_message
from ewcore.write_ew_hash import write_ew_hash


app = flask.Flask(__name__)
payment = Payment(app, Wallet())


@app.route('/hello')
@payment.required(1)
def hello():
    return 'Hello, world'


@app.route('/write-ew-message')
@payment.required(1)
def write_ew_message_endpoint():
    print("write_ew_message_endpoint()")
    msg = request.args.get('message')
    write_ew_message(msg)


@app.route('/write-ew-hash')
@payment.required(1)
def write_ew_hash_endpoint():
    print("write_ew_message_endpoint()")
    hash = request.args.get('hash')
    write_ew_hash(hash)


@app.route('/manifest')
def manifest():
    """Provide the app manifest to the two1 crawler."""
    with open('./manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

