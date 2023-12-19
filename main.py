from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Extract information from the GitHub payload
        data = json.loads(post_data)
        repo_name = data.get('repository', {}).get('name')
        commit_message = data.get('head_commit', {}).get('message')
        print(f"New commit in repository '{repo_name}': {commit_message}")

        # Send a response
        response_message = {'status': 'success'}
        self._send_response(200, response_message)

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=9090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

