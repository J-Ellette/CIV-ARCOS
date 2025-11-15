"""
WebSocket server for live quality score updates.
Provides real-time notifications of quality metric changes to connected clients.
"""

import json
import hashlib
import base64
import struct
import socket
import threading
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
from ..core.cache import get_cache


class WebSocketFrame:
    """Represents a WebSocket frame for protocol handling."""

    # Opcodes
    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xA

    def __init__(
        self,
        opcode: int = TEXT,
        payload: bytes = b"",
        fin: bool = True,
        mask: Optional[bytes] = None,
    ):
        """
        Initialize WebSocket frame.

        Args:
            opcode: Frame opcode
            payload: Frame payload data
            fin: Final frame flag
            mask: Optional masking key (4 bytes)
        """
        self.opcode = opcode
        self.payload = payload
        self.fin = fin
        self.mask = mask

    @classmethod
    def parse(cls, data: bytes) -> Optional["WebSocketFrame"]:
        """
        Parse WebSocket frame from bytes.

        Args:
            data: Raw frame data

        Returns:
            WebSocketFrame or None if incomplete
        """
        if len(data) < 2:
            return None

        # Parse first byte
        fin = (data[0] & 0x80) != 0
        opcode = data[0] & 0x0F

        # Parse second byte
        masked = (data[1] & 0x80) != 0
        payload_len = data[1] & 0x7F

        offset = 2

        # Extended payload length
        if payload_len == 126:
            if len(data) < offset + 2:
                return None
            payload_len = struct.unpack("!H", data[offset : offset + 2])[0]
            offset += 2
        elif payload_len == 127:
            if len(data) < offset + 8:
                return None
            payload_len = struct.unpack("!Q", data[offset : offset + 8])[0]
            offset += 8

        # Masking key
        mask = None
        if masked:
            if len(data) < offset + 4:
                return None
            mask = data[offset : offset + 4]
            offset += 4

        # Payload
        if len(data) < offset + payload_len:
            return None

        payload = data[offset : offset + payload_len]

        # Unmask payload
        if mask:
            payload = bytes(payload[i] ^ mask[i % 4] for i in range(len(payload)))

        return cls(opcode=opcode, payload=payload, fin=fin, mask=mask)

    def to_bytes(self) -> bytes:
        """
        Convert frame to bytes.

        Returns:
            Frame as bytes
        """
        # First byte: FIN + opcode
        b1 = (0x80 if self.fin else 0x00) | self.opcode

        # Second byte: MASK + payload length
        payload_len = len(self.payload)
        if payload_len < 126:
            b2 = payload_len
            extended_len = b""
        elif payload_len < 65536:
            b2 = 126
            extended_len = struct.pack("!H", payload_len)
        else:
            b2 = 127
            extended_len = struct.pack("!Q", payload_len)

        # We don't mask server->client frames
        header = bytes([b1, b2]) + extended_len

        return header + self.payload


class WebSocketConnection:
    """Represents a WebSocket client connection."""

    def __init__(self, sock: socket.socket, address: tuple):
        """
        Initialize WebSocket connection.

        Args:
            sock: Client socket
            address: Client address
        """
        self.sock = sock
        self.address = address
        self.connected = False
        self.subscriptions: Set[str] = set()

    def send_text(self, message: str) -> bool:
        """
        Send text message to client.

        Args:
            message: Text message

        Returns:
            True on success
        """
        try:
            frame = WebSocketFrame(
                opcode=WebSocketFrame.TEXT, payload=message.encode("utf-8")
            )
            self.sock.sendall(frame.to_bytes())
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def send_json(self, data: Dict[str, Any]) -> bool:
        """
        Send JSON message to client.

        Args:
            data: Dictionary to send as JSON

        Returns:
            True on success
        """
        return self.send_text(json.dumps(data))

    def close(self) -> None:
        """Close the connection."""
        try:
            frame = WebSocketFrame(opcode=WebSocketFrame.CLOSE)
            self.sock.sendall(frame.to_bytes())
        except:
            pass
        finally:
            self.connected = False
            try:
                self.sock.close()
            except:
                pass


class WebSocketServer:
    """
    WebSocket server for real-time quality score updates.
    Integrates with the cache pub/sub system for notifications.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8001):
        """
        Initialize WebSocket server.

        Args:
            host: Server host
            port: Server port
        """
        self.host = host
        self.port = port
        self.connections: List[WebSocketConnection] = []
        self.running = False
        self.server_socket: Optional[socket.socket] = None
        self.cache = get_cache()

        # Register for cache pub/sub notifications
        self.cache.subscribe("quality_update", self._on_quality_update)
        self.cache.subscribe("badge_update", self._on_badge_update)
        self.cache.subscribe("test_update", self._on_test_update)

    def _on_quality_update(self, channel: str, message: Any) -> None:
        """
        Handle quality score update from cache.

        Args:
            channel: Channel name
            message: Update message
        """
        self.broadcast(
            {
                "type": "quality_update",
                "channel": channel,
                "data": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def _on_badge_update(self, channel: str, message: Any) -> None:
        """
        Handle badge update from cache.

        Args:
            channel: Channel name
            message: Update message
        """
        self.broadcast(
            {
                "type": "badge_update",
                "channel": channel,
                "data": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def _on_test_update(self, channel: str, message: Any) -> None:
        """
        Handle test result update from cache.

        Args:
            channel: Channel name
            message: Update message
        """
        self.broadcast(
            {
                "type": "test_update",
                "channel": channel,
                "data": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def start(self) -> None:
        """Start the WebSocket server."""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"WebSocket server listening on {self.host}:{self.port}")

        # Start accept thread
        accept_thread = threading.Thread(target=self._accept_connections)
        accept_thread.daemon = True
        accept_thread.start()

    def stop(self) -> None:
        """Stop the WebSocket server."""
        self.running = False

        # Close all connections
        for conn in self.connections[:]:
            conn.close()
        self.connections.clear()

        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

    def _accept_connections(self) -> None:
        """Accept incoming connections."""
        while self.running:
            try:
                if not self.server_socket:
                    break

                self.server_socket.settimeout(1.0)
                try:
                    client_sock, address = self.server_socket.accept()
                except socket.timeout:
                    continue

                # Handle connection in a new thread
                thread = threading.Thread(
                    target=self._handle_connection, args=(client_sock, address)
                )
                thread.daemon = True
                thread.start()

            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")

    def _handle_connection(self, client_sock: socket.socket, address: tuple) -> None:
        """
        Handle a client connection.

        Args:
            client_sock: Client socket
            address: Client address
        """
        conn = WebSocketConnection(client_sock, address)

        try:
            # Perform WebSocket handshake
            if not self._perform_handshake(client_sock):
                client_sock.close()
                return

            conn.connected = True
            self.connections.append(conn)

            print(f"WebSocket client connected from {address}")

            # Send welcome message
            conn.send_json(
                {
                    "type": "welcome",
                    "message": "Connected to CIV-ARCOS WebSocket server",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )

            # Handle incoming messages
            buffer = b""
            while self.running and conn.connected:
                try:
                    client_sock.settimeout(1.0)
                    data = client_sock.recv(4096)
                    if not data:
                        break

                    buffer += data
                    frame = WebSocketFrame.parse(buffer)

                    if frame:
                        buffer = buffer[len(frame.to_bytes()) :]
                        self._handle_frame(conn, frame)

                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    break

        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            # Clean up
            if conn in self.connections:
                self.connections.remove(conn)
            conn.close()
            print(f"WebSocket client disconnected from {address}")

    def _perform_handshake(self, client_sock: socket.socket) -> bool:
        """
        Perform WebSocket handshake.

        Args:
            client_sock: Client socket

        Returns:
            True on success
        """
        try:
            # Read HTTP request
            request = b""
            while b"\r\n\r\n" not in request:
                chunk = client_sock.recv(1024)
                if not chunk:
                    return False
                request += chunk

            # Parse request headers
            headers = {}
            lines = request.decode("utf-8").split("\r\n")
            for line in lines[1:]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip().lower()] = value.strip()

            # Get WebSocket key
            ws_key = headers.get("sec-websocket-key")
            if not ws_key:
                return False

            # Generate accept key
            magic = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            accept = base64.b64encode(
                hashlib.sha1((ws_key + magic).encode()).digest()
            ).decode()

            # Send handshake response
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept}\r\n"
                "\r\n"
            )
            client_sock.sendall(response.encode())

            return True

        except Exception as e:
            print(f"Handshake error: {e}")
            return False

    def _handle_frame(self, conn: WebSocketConnection, frame: WebSocketFrame) -> None:
        """
        Handle incoming WebSocket frame.

        Args:
            conn: Connection
            frame: Received frame
        """
        if frame.opcode == WebSocketFrame.TEXT:
            try:
                message = json.loads(frame.payload.decode("utf-8"))
                self._handle_message(conn, message)
            except Exception as e:
                print(f"Error handling text frame: {e}")

        elif frame.opcode == WebSocketFrame.CLOSE:
            conn.connected = False

        elif frame.opcode == WebSocketFrame.PING:
            # Respond with pong
            pong = WebSocketFrame(opcode=WebSocketFrame.PONG, payload=frame.payload)
            conn.sock.sendall(pong.to_bytes())

    def _handle_message(self, conn: WebSocketConnection, message: Dict[str, Any]) -> None:
        """
        Handle incoming JSON message.

        Args:
            conn: Connection
            message: JSON message
        """
        msg_type = message.get("type")

        if msg_type == "subscribe":
            # Subscribe to a channel
            channel = message.get("channel")
            if channel:
                conn.subscriptions.add(channel)
                conn.send_json(
                    {"type": "subscribed", "channel": channel, "success": True}
                )

        elif msg_type == "unsubscribe":
            # Unsubscribe from a channel
            channel = message.get("channel")
            if channel and channel in conn.subscriptions:
                conn.subscriptions.remove(channel)
                conn.send_json(
                    {"type": "unsubscribed", "channel": channel, "success": True}
                )

        elif msg_type == "ping":
            # Respond to ping
            conn.send_json({"type": "pong"})

    def broadcast(self, message: Dict[str, Any]) -> int:
        """
        Broadcast message to all connected clients.

        Args:
            message: Message to broadcast

        Returns:
            Number of clients that received the message
        """
        count = 0
        for conn in self.connections[:]:
            if conn.connected:
                if conn.send_json(message):
                    count += 1
        return count

    def send_to_channel(self, channel: str, message: Dict[str, Any]) -> int:
        """
        Send message to clients subscribed to a channel.

        Args:
            channel: Channel name
            message: Message to send

        Returns:
            Number of clients that received the message
        """
        count = 0
        for conn in self.connections[:]:
            if conn.connected and channel in conn.subscriptions:
                if conn.send_json(message):
                    count += 1
        return count


# Global WebSocket server instance
_ws_server: Optional[WebSocketServer] = None


def get_websocket_server(
    host: str = "0.0.0.0", port: int = 8001
) -> WebSocketServer:
    """
    Get global WebSocket server instance (singleton).

    Args:
        host: Server host
        port: Server port

    Returns:
        WebSocketServer instance
    """
    global _ws_server
    if _ws_server is None:
        _ws_server = WebSocketServer(host, port)
    return _ws_server
