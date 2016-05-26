import json

import flask
import yaml
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


@app.route('/ew/message')
@payment.required(1000)
def write_ew_message_endpoint():
    print("write_ew_message_endpoint()")
    msg = request.args.get('message')
    write_ew_message(msg)
    return msg


@app.route('/ew/hash', methods=['GET', 'POST'])
@payment.required(1000)
def ew_hash():
    print("ew_hash() " + request.method)
    hash_value = request.args.get('hash')
    print("hash_value=" + hash_value)
    if not is_hash(hash_value):
        abort(400)

    if request.method == 'POST':
        return ew_post_hash(hash_value)
    else:
        return ew_get_hash(hash_value)


@app.route('/manifest')
def manifest():
    """Provide the app manifest to the two1 crawler."""
    with open('./manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


