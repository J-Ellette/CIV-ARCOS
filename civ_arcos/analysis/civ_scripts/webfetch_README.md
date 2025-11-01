# WebFetch - HTTP Client

HTTP client for Python development using urllib.

## Description

WebFetch provides functionality for making HTTP requests without external libraries like requests.

## Usage

```python
from civ_arcos.analysis.civ_scripts.webfetch import WebFetch

fetcher = WebFetch()

# GET request
response = fetcher.get('https://api.example.com/data')
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

# POST JSON data
data = {'key': 'value'}
response = fetcher.post_json('https://api.example.com/data', data)

# Download file
bytes_downloaded = fetcher.download('https://example.com/file.zip', 'local.zip')

# URL encoding
encoded = fetcher.quote('hello world')
decoded = fetcher.unquote(encoded)

# Parse URL
parsed = fetcher.urlparse('https://example.com/path?query=value')
```

## Features

- HTTP GET, POST, PUT, DELETE requests
- JSON request/response handling
- File downloads
- URL encoding/decoding
- URL parsing and construction
- Query string handling
- Custom headers support
- Timeout support

## API Reference

### HTTP Methods

- `get(url, headers=None, timeout=None)` - Send GET request
- `post(url, data=None, headers=None, timeout=None)` - Send POST request
- `put(url, data=None, headers=None, timeout=None)` - Send PUT request
- `delete(url, headers=None, timeout=None)` - Send DELETE request
- `request(method, url, ...)` - Send generic HTTP request

### JSON Methods

- `get_json(url, ...)` - GET request and parse JSON response
- `post_json(url, data, ...)` - POST JSON data and parse response

### File Methods

- `download(url, filename, headers=None)` - Download file from URL
- `urlopen(url, data=None, timeout=None)` - Open URL (like urllib.request.urlopen)

### URL Utilities

- `quote(string, safe='/')` - URL-encode string
- `unquote(string)` - URL-decode string
- `urlencode(query)` - Encode dictionary as query string
- `parse_qs(qs)` - Parse query string into dictionary
- `urlparse(url)` - Parse URL into components
- `urlunparse(components)` - Construct URL from components
- `urljoin(base, url)` - Join base URL with relative URL

## Response Object

The `WebFetchResponse` object has:
- `status_code` - HTTP status code
- `headers` - Response headers dictionary
- `url` - Final URL (after redirects)
- `text` - Response body as text
- `read()` - Read response body as bytes
- `json()` - Parse response body as JSON

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.webfetch
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
