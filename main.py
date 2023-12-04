from flask import Flask, request, abort
import hmac
import hashlib
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the GitHub webhook secret from the environment variable
webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET')


@app.route('/webhook', methods=['POST'])
def webhook():
    # Validate GitHub signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not is_valid_signature(request.data, signature):
        abort(403, 'Invalid signature')

    # Parse the JSON payload
    payload = request.get_json()

    # Process the payload and handle changes
    print('Received GitHub webhook:', payload)
    # Add your logic to handle changes here

    return 'Webhook received successfully', 200


def is_valid_signature(data, signature):
    expected_signature = 'sha256=' + hmac.new(webhook_secret.encode(), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_signature)


if __name__ == '__main__':
    app.run(port=3000)
