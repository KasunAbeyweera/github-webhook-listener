from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint that receives GitHub webhooks.

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            repository:
              type: object
              properties:
                name:
                  type: string
                # Add more properties as needed
            head_commit:
              type: object
              properties:
                message:
                  type: string
                # Add more properties as needed
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            status:
              type: string
    """
    data = request.json  # Assuming the incoming data is in JSON format

    # Extract information from the GitHub payload
    repo_name = data.get('repository', {}).get('name')
    commit_message = data.get('head_commit', {}).get('message')
    print(f"New commit in repository '{repo_name}': {commit_message}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    port = 9090
    app.run(debug=True, port=port)
