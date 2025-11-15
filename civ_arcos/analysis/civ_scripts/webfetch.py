"""WebFetch - URL fetcher

HTTP client for development tasks.
Wrapper around Python's urllib module for HTTP requests.
"""

import urllib.request
import urllib.parse
import urllib.error
from typing import Any, Dict, List, Optional, Union
import json as _json


class WebFetchResponse:
    """Response from HTTP request"""
    
    def __init__(self, response):
        """Initialize from urllib response"""
        self._response = response
        self._content = None
    
    @property
    def status_code(self) -> int:
        """Get HTTP status code"""
        return self._response.status
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get response headers"""
        return dict(self._response.headers)
    
    @property
    def url(self) -> str:
        """Get final URL (after redirects)"""
        return self._response.url
    
    def read(self) -> bytes:
        """Read response body as bytes"""
        if self._content is None:
            self._content = self._response.read()
        return self._content
    
    @property
    def text(self) -> str:
        """Get response body as text"""
        content = self.read()
        encoding = self._response.headers.get_content_charset('utf-8')
        return content.decode(encoding)
    
    def json(self) -> Any:
        """Parse response body as JSON"""
        return _json.loads(self.text)


class WebFetch:
    """
    WebFetch: URL fetcher
    
    Provides utilities for HTTP requests using urllib.
    """
    
    def __init__(self):
        """Initialize WebFetch"""
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
    
    def get(self, 
            url: str, 
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[float] = None) -> WebFetchResponse:
        """
        Send GET request.
        
        Args:
            url: URL to request
            headers: Request headers
            timeout: Request timeout in seconds
            
        Returns:
            WebFetchResponse object
        """
        return self.request('GET', url, headers=headers, timeout=timeout)
    
    def post(self, 
             url: str,
             data: Optional[Union[Dict, bytes, str]] = None,
             headers: Optional[Dict[str, str]] = None,
             timeout: Optional[float] = None) -> WebFetchResponse:
        """
        Send POST request.
        
        Args:
            url: URL to request
            data: Request body
            headers: Request headers
            timeout: Request timeout in seconds
            
        Returns:
            WebFetchResponse object
        """
        return self.request('POST', url, data=data, headers=headers, timeout=timeout)
    
    def put(self, 
            url: str,
            data: Optional[Union[Dict, bytes, str]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[float] = None) -> WebFetchResponse:
        """
        Send PUT request.
        
        Args:
            url: URL to request
            data: Request body
            headers: Request headers
            timeout: Request timeout in seconds
            
        Returns:
            WebFetchResponse object
        """
        return self.request('PUT', url, data=data, headers=headers, timeout=timeout)
    
    def delete(self, 
               url: str,
               headers: Optional[Dict[str, str]] = None,
               timeout: Optional[float] = None) -> WebFetchResponse:
        """
        Send DELETE request.
        
        Args:
            url: URL to request
            headers: Request headers
            timeout: Request timeout in seconds
            
        Returns:
            WebFetchResponse object
        """
        return self.request('DELETE', url, headers=headers, timeout=timeout)
    
    def request(self,
                method: str,
                url: str,
                data: Optional[Union[Dict, bytes, str]] = None,
                headers: Optional[Dict[str, str]] = None,
                timeout: Optional[float] = None) -> WebFetchResponse:
        """
        Send HTTP request.
        
        Args:
            method: HTTP method
            url: URL to request
            data: Request body
            headers: Request headers
            timeout: Request timeout in seconds
            
        Returns:
            WebFetchResponse object
        """
        # Prepare data
        if data is not None:
            if isinstance(data, dict):
                data = urllib.parse.urlencode(data).encode('utf-8')
            elif isinstance(data, str):
                data = data.encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url, data=data, method=method)
        
        # Add headers
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        # Send request
        try:
            response = urllib.request.urlopen(req, timeout=timeout)
            self.request_count += 1
            self.success_count += 1
            return WebFetchResponse(response)
        except urllib.error.HTTPError as e:
            self.request_count += 1
            self.error_count += 1
            raise
        except urllib.error.URLError as e:
            self.request_count += 1
            self.error_count += 1
            raise
    
    def download(self, 
                 url: str, 
                 filename: str,
                 headers: Optional[Dict[str, str]] = None) -> int:
        """
        Download file from URL.
        
        Args:
            url: URL to download from
            filename: Local filename to save to
            headers: Request headers
            
        Returns:
            Number of bytes downloaded
        """
        req = urllib.request.Request(url)
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        try:
            with urllib.request.urlopen(req) as response:
                with open(filename, 'wb') as f:
                    content = response.read()
                    f.write(content)
            
            self.request_count += 1
            self.success_count += 1
            return len(content)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            self.request_count += 1
            self.error_count += 1
            raise
    
    def urlopen(self, 
                url: str,
                data: Optional[bytes] = None,
                timeout: Optional[float] = None):
        """
        Open URL (like urllib.request.urlopen).
        
        Args:
            url: URL to open
            data: Request data
            timeout: Request timeout
            
        Returns:
            Response object
        """
        try:
            response = urllib.request.urlopen(url, data=data, timeout=timeout)
            self.request_count += 1
            self.success_count += 1
            return response
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            self.request_count += 1
            self.error_count += 1
            raise
    
    def quote(self, string: str, safe: str = '/') -> str:
        """
        URL-encode string.
        
        Args:
            string: String to encode
            safe: Characters not to encode
            
        Returns:
            URL-encoded string
        """
        return urllib.parse.quote(string, safe=safe)
    
    def unquote(self, string: str) -> str:
        """
        URL-decode string.
        
        Args:
            string: String to decode
            
        Returns:
            Decoded string
        """
        return urllib.parse.unquote(string)
    
    def urlencode(self, query: Dict[str, Any]) -> str:
        """
        Encode dictionary as URL query string.
        
        Args:
            query: Dictionary to encode
            
        Returns:
            URL-encoded query string
        """
        return urllib.parse.urlencode(query)
    
    def parse_qs(self, qs: str) -> Dict[str, List[str]]:
        """
        Parse query string into dictionary.
        
        Args:
            qs: Query string
            
        Returns:
            Dictionary of parsed values
        """
        return urllib.parse.parse_qs(qs)
    
    def urlparse(self, url: str):
        """
        Parse URL into components.
        
        Args:
            url: URL to parse
            
        Returns:
            ParseResult with URL components
        """
        return urllib.parse.urlparse(url)
    
    def urlunparse(self, components: tuple) -> str:
        """
        Construct URL from components.
        
        Args:
            components: URL components tuple
            
        Returns:
            Constructed URL
        """
        return urllib.parse.urlunparse(components)
    
    def urljoin(self, base: str, url: str) -> str:
        """
        Join base URL with relative URL.
        
        Args:
            base: Base URL
            url: Relative URL
            
        Returns:
            Absolute URL
        """
        return urllib.parse.urljoin(base, url)
    
    def get_json(self, 
                 url: str,
                 headers: Optional[Dict[str, str]] = None,
                 timeout: Optional[float] = None) -> Any:
        """
        GET request and parse JSON response.
        
        Args:
            url: URL to request
            headers: Request headers
            timeout: Request timeout
            
        Returns:
            Parsed JSON data
        """
        response = self.get(url, headers=headers, timeout=timeout)
        return response.json()
    
    def post_json(self,
                  url: str,
                  data: Dict,
                  headers: Optional[Dict[str, str]] = None,
                  timeout: Optional[float] = None) -> Any:
        """
        POST JSON data and parse JSON response.
        
        Args:
            url: URL to request
            data: Dictionary to send as JSON
            headers: Request headers
            timeout: Request timeout
            
        Returns:
            Parsed JSON response
        """
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json'
        
        json_data = _json.dumps(data).encode('utf-8')
        response = self.post(url, data=json_data, headers=headers, timeout=timeout)
        return response.json()
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'total_requests': self.request_count,
            'successful': self.success_count,
            'errors': self.error_count
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        return {
            'total_requests': self.request_count,
            'successful_requests': self.success_count,
            'failed_requests': self.error_count,
            'success_rate': (
                self.success_count / self.request_count 
                if self.request_count > 0 else 0
            )
        }
