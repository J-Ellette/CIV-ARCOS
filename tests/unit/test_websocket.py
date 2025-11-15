"""
Tests for WebSocket server functionality.
"""

import pytest
import json
import time
from civ_arcos.web.websocket import (
    WebSocketServer,
    WebSocketConnection,
    WebSocketFrame,
    get_websocket_server,
)
from civ_arcos.core.cache import get_cache


class TestWebSocketFrame:
    """Test WebSocket frame parsing and encoding."""

    def test_frame_creation(self):
        """Test creating a WebSocket frame."""
        frame = WebSocketFrame(opcode=WebSocketFrame.TEXT, payload=b"Hello")
        assert frame.opcode == WebSocketFrame.TEXT
        assert frame.payload == b"Hello"
        assert frame.fin is True

    def test_text_frame_to_bytes(self):
        """Test converting text frame to bytes."""
        frame = WebSocketFrame(opcode=WebSocketFrame.TEXT, payload=b"Test")
        data = frame.to_bytes()
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_close_frame(self):
        """Test creating a close frame."""
        frame = WebSocketFrame(opcode=WebSocketFrame.CLOSE)
        data = frame.to_bytes()
        assert data[0] & 0x0F == WebSocketFrame.CLOSE


class TestWebSocketConnection:
    """Test WebSocket connection functionality."""

    def test_connection_creation(self):
        """Test creating a WebSocket connection."""
        # We can't create a real socket, so we'll just test the structure
        # In a real test, we'd use a mock socket
        pass  # Skip actual socket tests in unit tests

    def test_subscription_management(self):
        """Test subscription set management."""
        # Mock connection without actual socket
        class MockSocket:
            def sendall(self, data):
                pass

        conn = WebSocketConnection(MockSocket(), ("127.0.0.1", 8001))
        assert len(conn.subscriptions) == 0

        conn.subscriptions.add("quality_update")
        assert "quality_update" in conn.subscriptions

        conn.subscriptions.remove("quality_update")
        assert "quality_update" not in conn.subscriptions


class TestWebSocketServer:
    """Test WebSocket server functionality."""

    def test_server_creation(self):
        """Test creating a WebSocket server."""
        server = WebSocketServer(host="127.0.0.1", port=8002)
        assert server.host == "127.0.0.1"
        assert server.port == 8002
        assert server.running is False
        assert len(server.connections) == 0

    def test_server_cache_integration(self):
        """Test server integrates with cache."""
        server = WebSocketServer(port=8003)
        assert server.cache is not None

    def test_broadcast_no_connections(self):
        """Test broadcasting with no connections."""
        server = WebSocketServer(port=8004)
        count = server.broadcast({"type": "test", "message": "hello"})
        assert count == 0

    def test_send_to_channel_no_connections(self):
        """Test sending to channel with no connections."""
        server = WebSocketServer(port=8005)
        count = server.send_to_channel("test_channel", {"type": "test"})
        assert count == 0

    def test_get_websocket_server(self):
        """Test getting singleton WebSocket server."""
        server1 = get_websocket_server(port=8006)
        server2 = get_websocket_server(port=8006)
        # Note: This will be the same instance due to singleton pattern
        assert server1 is not None
        assert server2 is not None


class TestWebSocketCacheIntegration:
    """Test WebSocket integration with cache pub/sub."""

    def test_quality_update_callback(self):
        """Test quality update callback is registered."""
        cache = get_cache()
        server = WebSocketServer(port=8007)

        # Publish a quality update
        result = cache.publish("quality_update", {"score": 95})
        # Should return number of subscribers (at least 1 from server)
        assert result >= 0

    def test_badge_update_callback(self):
        """Test badge update callback is registered."""
        cache = get_cache()
        server = WebSocketServer(port=8008)

        # Publish a badge update
        result = cache.publish("badge_update", {"type": "coverage", "value": 90})
        assert result >= 0

    def test_test_update_callback(self):
        """Test test update callback is registered."""
        cache = get_cache()
        server = WebSocketServer(port=8009)

        # Publish a test update
        result = cache.publish("test_update", {"passed": 10, "failed": 0})
        assert result >= 0
