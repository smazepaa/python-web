from urllib.parse import urlparse, parse_qs


def parse_url(url):
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return {'error': 'Invalid URL: Missing http/https scheme.'}

        if not parsed_url.netloc:
            return {'error': 'Invalid URL: Missing domain name.'}

        # splitting path components and queries
        path_components = parsed_url.path.strip('/').split('/') if parsed_url.path.strip('/') else []
        query_params = parse_qs(parsed_url.query)

        # dynamically setting the key based on the content
        path_param_key = f"Path to the Resource ({len(path_components)} steps)" if path_components \
            else "Path to the Resource"
        query_param_key = f"Query Parameters ({len(query_params)})" if query_params else "Query Parameters"

        # structuring the response as JSON
        response = {
            'URL Analysis':
                {
                    'URL': url,
                    'Protocol': parsed_url.scheme,
                    'Domain': parsed_url.netloc,
                    path_param_key: ' > '.join(path_components) if path_components else 'None',
                    query_param_key: {param: ', '.join(values) for param, values in query_params.items()}
                                    if query_params else 'None'
                }
        }

        return response
    except Exception as e:
        return {'error': f'Error parsing URL: {e}'}
