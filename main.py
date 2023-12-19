from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Assuming the incoming data is in JSON format

    # Extract information from the GitHub payload
    repo_name = data.get('repository', {}).get('name')
    commit_message = data.get('head_commit', {}).get('message')
    print(f"New commit in repository '{repo_name}': {commit_message}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    port = 9090
    app.run(debug=True, port=port)