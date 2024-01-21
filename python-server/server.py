from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import mimetypes

from helpers.parseUrl import parse_url


class SimpleHandler(SimpleHTTPRequestHandler):
    def _send_response(self, message, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if content_type == 'application/json':
            self.wfile.write(bytes(json.dumps(message), 'utf8'))
        elif content_type == 'text/html':
            self.wfile.write(bytes(message, 'utf8'))
        else:
            self.wfile.write(message.read())

    def _process_url(self, url):
        url_info = parse_url(url)
        if 'error' in url_info:
            self._send_response(url_info, status=400)
        else:
            self._send_response(url_info, content_type='application/json')

    def _send_file(self, filename):
        file_path = 'assets/images/' + filename

        content_type = mimetypes.guess_type(file_path)[0]
        print(content_type)

        try:
            with open(file_path, 'rb') as file:
                self._send_response(file, content_type=content_type)
        except IOError:
            self._send_response({'error': 'File not found'}, status=404, content_type='application/json')

    def do_GET(self):
        print(self.path)

        if self.path.startswith('/image/'):
            self._send_file(self.path[len('/image/'):])

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)

        if self.path == '/parse-url':
            # decoding the received data from bytes to string
            url = post_data.decode('utf-8').strip()
            if url:
                self._process_url(url)
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
