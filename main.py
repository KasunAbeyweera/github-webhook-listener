from flask import Flask, request, abort
import hmac
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET')


@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not is_valid_signature(request.data, signature):
        abort(403, 'Invalid signature')

    payload = request.get_json()

    print('Received GitHub webhook:', payload)

    return 'Webhook received successfully', 200


def is_valid_signature(data, signature):
    expected_signature = 'sha256=' + hmac.new(webhook_secret.encode(), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_signature)


if __name__ == '__main__':
    app.run(port=3000)
