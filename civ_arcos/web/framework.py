"""
Minimal web framework for CIV-ARCOS.
Emulates FastAPI/Flask without external dependencies.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse


class Request:
    """Represents an HTTP request."""

    def __init__(
        self, method: str, path: str, query: Dict[str, List[str]], body: bytes
    ):
        self.method = method
        self.path = path
        self.query = query
        self.body = body
        self._json = None

    def json(self) -> Dict[str, Any]:
        """Parse request body as JSON."""
        if self._json is None and self.body:
            self._json = json.loads(self.body.decode())
        return self._json or {}


class Response:
    """Represents an HTTP response."""

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        content_type: str = "application/json",
    ):
        self.content = content
        self.status_code = status_code
        self.content_type = content_type

    def to_bytes(self) -> bytes:
        """Convert response to bytes."""
        if isinstance(self.content, (dict, list)):
            return json.dumps(self.content).encode()
        elif isinstance(self.content, str):
            return self.content.encode()
        elif isinstance(self.content, bytes):
            return self.content
        return b""


class Router:
    """Simple URL router."""

    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}

    def add_route(self, method: str, path: str, handler: Callable) -> None:
        """
        Add a route to the router.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: URL path
            handler: Handler function
        """
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = handler

    def get(self, path: str) -> Callable:
        """Decorator for GET routes."""

        def decorator(handler: Callable) -> Callable:
            self.add_route("GET", path, handler)
            return handler

        return decorator

    def post(self, path: str) -> Callable:
        """Decorator for POST routes."""

        def decorator(handler: Callable) -> Callable:
            self.add_route("POST", path, handler)
            return handler

        return decorator

    def put(self, path: str) -> Callable:
        """Decorator for PUT routes."""

        def decorator(handler: Callable) -> Callable:
            self.add_route("PUT", path, handler)
            return handler

        return decorator

    def delete(self, path: str) -> Callable:
        """Decorator for DELETE routes."""

        def decorator(handler: Callable) -> Callable:
            self.add_route("DELETE", path, handler)
            return handler

        return decorator

    def route(self, request: Request) -> Tuple[Optional[Callable], Dict[str, str]]:
        """
        Find handler for request.

        Args:
            request: HTTP request

        Returns:
            Tuple of (handler, path_params) or (None, {})
        """
        # Try exact match first
        if request.path in self.routes:
            handlers = self.routes[request.path]
            if request.method in handlers:
                return handlers[request.method], {}

        # Try pattern matching for path parameters
        for route_path, handlers in self.routes.items():
            params = self._match_path(route_path, request.path)
            if params is not None and request.method in handlers:
                return handlers[request.method], params

        return None, {}

    def _match_path(self, pattern: str, path: str) -> Optional[Dict[str, str]]:
        """
        Match path against pattern with parameters.

        Args:
            pattern: Route pattern (e.g., "/api/badge/{repo}/{branch}")
            path: Actual path

        Returns:
            Dictionary of path parameters or None if no match
        """
        pattern_parts = pattern.split("/")
        path_parts = path.split("/")

        if len(pattern_parts) != len(path_parts):
            return None

        params = {}
        for pattern_part, path_part in zip(pattern_parts, path_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                # Extract parameter name
                param_name = pattern_part[1:-1]
                params[param_name] = path_part
            elif pattern_part != path_part:
                return None

        return params


class Application:
    """Simple web application."""

    def __init__(self):
        self.router = Router()

    def get(self, path: str) -> Callable:
        """Decorator for GET routes."""
        return self.router.get(path)

    def post(self, path: str) -> Callable:
        """Decorator for POST routes."""
        return self.router.post(path)

    def put(self, path: str) -> Callable:
        """Decorator for PUT routes."""
        return self.router.put(path)

    def delete(self, path: str) -> Callable:
        """Decorator for DELETE routes."""
        return self.router.delete(path)

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """
        Run the web server.

        Args:
            host: Host to bind to
            port: Port to bind to
        """
        handler_class = self._create_handler_class()
        server = HTTPServer((host, port), handler_class)

        print(f"Starting CIV-ARCOS server on {host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server.shutdown()

    def _create_handler_class(self):
        """Create a request handler class with access to the router."""
        router = self.router

        class RequestHandler(BaseHTTPRequestHandler):
            """Handle HTTP requests."""

            def do_GET(self):
                self._handle_request("GET")

            def do_POST(self):
                self._handle_request("POST")

            def do_PUT(self):
                self._handle_request("PUT")

            def do_DELETE(self):
                self._handle_request("DELETE")

            def _handle_request(self, method: str):
                """Handle an HTTP request."""
                # Parse URL
                parsed = urlparse(self.path)
                query = parse_qs(parsed.query)

                # Read body
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length) if content_length > 0 else b""

                # Create request object
                request = Request(method, parsed.path, query, body)

                # Find handler
                handler, path_params = router.route(request)

                if handler:
                    try:
                        # Call handler
                        response = handler(request, **path_params)

                        # Ensure response is a Response object
                        if not isinstance(response, Response):
                            response = Response(response)

                        # Send response
                        self.send_response(response.status_code)
                        self.send_header("Content-Type", response.content_type)
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(response.to_bytes())

                    except Exception as e:
                        # Handle errors
                        self.send_error(500, f"Internal Server Error: {str(e)}")
                else:
                    # 404 Not Found
                    self.send_error(404, "Not Found")

            def log_message(self, format, *args):
                """Override to customize logging."""
                print(f"{self.address_string()} - {format % args}")

        return RequestHandler


def create_app() -> Application:
    """Create a new web application instance."""
    return Application()
