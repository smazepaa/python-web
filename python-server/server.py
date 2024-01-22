from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import mimetypes

from helpers.parseUrl import parse_url
from helpers.analyzeText import analyze_text
from helpers.parseParts import parse_parts


class SimpleHandler(SimpleHTTPRequestHandler):
    def _send_response(self, message, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if content_type == 'application/json':
            # Ensure that JSON data is sent as a JSON object
            if isinstance(message, dict):
                self.wfile.write(bytes(json.dumps(message), 'utf8'))
            else:
                self.wfile.write(bytes(message, 'utf8'))
        elif content_type == 'text/html':
            self.wfile.write(bytes(message, 'utf8'))
        else:  # means it's a file
            self.wfile.write(message.read())

    def _process_url(self, url):
        url_info = parse_url(url)
        if 'error' in url_info:
            self._send_response(url_info, status=400, content_type='application/json')
        else:
            self._send_response(url_info, content_type='application/json')

    def _send_image(self, filename):
        file_path = 'assets/images/' + filename
        content_type = mimetypes.guess_type(file_path)[0]

        try:
            with open(file_path, 'rb') as file:
                self._send_response(file, content_type=content_type)
        except IOError:
            self._send_response({'error': 'File not found'}, status=404, content_type='application/json')

    def _send_json_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                # Parse the JSON file content
                json_content = json.load(file)

                # Convert JSON object to a formatted string (pretty print)
                formatted_json = json.dumps(json_content, indent=4)

                self._send_response(formatted_json, content_type='application/json')
        except IOError:
            self._send_response({'error': 'File not found'}, status=404, content_type='application/json')
        except json.JSONDecodeError:
            self._send_response({'error': 'Invalid JSON format'}, status=500, content_type='application/json')

    def _parse_multipart(self, data):
        content_type = self.headers['Content-Type']
        if not content_type.startswith('multipart/form-data;'):
            return None

        boundary = content_type.split('boundary=')[1].encode()

        # Splitting data into parts, excluding the first and last part
        parts = data.split(b'--' + boundary)[1:-1]
        return parse_parts(parts)

    def do_GET(self):

        if self.path == '/':
            self._send_json_file('./assets/documentation/info.json')

        if self.path.startswith('/image/'):
            self._send_image(self.path[len('/image/'):])

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        if self.path == '/parse-url':
            # decoding the received data from bytes to string
            url = post_data.decode('utf-8').strip()
            if url:
                self._process_url(url)
            else:
                self._send_response({'error': 'No URL provided in the POST request.'}, status=400,
                                    content_type='application/json')

        if self.path == '/parse-txt':
            parsed_data = self._parse_multipart(post_data)

            # Extract file and string data from parsed data
            file_data = parsed_data.get('file')
            search_string = parsed_data.get('string')

            if file_data and search_string:
                metadata = analyze_text(file_data, search_string)
                self._send_response(metadata, content_type='application/json')
            else:
                self._send_response({'error': 'Missing text file or search string'}, status=400,
                                    content_type='application/json')

        else:
            self._send_response({'error': 'Invalid path'}, status=404, content_type='application/json')


def run_server(port=4000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
