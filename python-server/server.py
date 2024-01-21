from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

from helpers.parseUrl import parse_url


class SimpleHandler(SimpleHTTPRequestHandler):
    def _send_response(self, message, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if content_type == 'application/json':
            self.wfile.write(bytes(json.dumps(message), 'utf8'))
        else:
            self.wfile.write(bytes(message, 'utf8'))

    def _process_request(self, url):
        url_info = parse_url(url)
        if 'error' in url_info:
            self._send_response(url_info, status=400)
        else:
            self._send_response(url_info, content_type='application/json')

    def do_GET(self):
        print(self.path)

        if self.path == '/text':
            self._send_response('Simple text')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)

        if self.path == '/parse-url':
            # decoding the received data from bytes to string
            url = post_data.decode('utf-8').strip()
            if url:
                self._process_request(url)
            else:
                self._send_response({'error': 'No URL provided in the POST request.'}, status=400)

        else:
            self._send_response({'error': 'Invalid path'}, status=404)


def run_server(port=4000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
