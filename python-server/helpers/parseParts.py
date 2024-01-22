import re


def parse_parts(parts):
    parsed_parts = {}

    for part in parts:
        # Splitting header and body
        if b'\r\n\r\n' in part:
            headers, body = part.split(b'\r\n\r\n', 1)
            body = body.rstrip(b'\r\n')  # Remove trailing new line characters

            # Extracting name and optionally filename from headers
            name = None
            for header in headers.split(b'\r\n'):
                if b'Content-Disposition' in header:
                    name = re.findall(r'name="([^"]+)"', header.decode())[0]
                    parsed_parts[name] = body.decode('utf-8')  # Decoding to string

    return parsed_parts
