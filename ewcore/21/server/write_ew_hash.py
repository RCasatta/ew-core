import flask
from two1.wallet import Wallet
from two1.bitserv.flask import Payment
import yaml
import json

app = flask.Flask(__name__)
payment = Payment(app, Wallet())


@app.route('/hello')
@payment.required(5000)
def hello():
    return 'Hello, world'

@app.route('/manifest')
def manifest():
    """Provide the app manifest to the 21 crawler.
    """
    with open('./manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#https://21.co/learn/intro-to-21/#create-your-first-bitcoin-payable-api
