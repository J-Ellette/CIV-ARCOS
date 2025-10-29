"""
Cache layer for real-time updates and performance optimization.
Emulates Redis functionality without external dependencies.
"""

import json
import time
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone, timedelta
from threading import Lock


class CacheEntry:
    """Represents a single cache entry with expiration."""

    def __init__(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Initialize cache entry.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None = no expiration)
        """
        self.key = key
        self.value = value
        self.created_at = datetime.now(timezone.utc)
        self.expires_at = (
            self.created_at + timedelta(seconds=ttl) if ttl else None
        )

    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


class RedisEmulator:
    """
    In-memory cache emulating Redis functionality.
    Provides caching for real-time updates and performance optimization.
    Thread-safe implementation.
    """

    def __init__(self):
        """Initialize Redis emulator."""
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = Lock()
        self._pubsub_channels: Dict[str, List[callable]] = {}

    def set(
        self, key: str, value: Any, ttl: Optional[int] = None, serialize: bool = True
    ) -> bool:
        """
        Set a value in cache with optional TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None = no expiration)
            serialize: Whether to JSON serialize the value

        Returns:
            True on success
        """
        with self._lock:
            if serialize and not isinstance(value, str):
                value = json.dumps(value)

            self._cache[key] = CacheEntry(key, value, ttl)
            return True

    def get(self, key: str, deserialize: bool = True) -> Optional[Any]:
        """
        Get a value from cache.

        Args:
            key: Cache key
            deserialize: Whether to JSON deserialize the value

        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None

            if entry.is_expired():
                del self._cache[key]
                return None

            value = entry.value
            if deserialize and isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass

            return value

    def delete(self, key: str) -> bool:
        """
        Delete a key from cache.

        Args:
            key: Cache key

        Returns:
            True if key existed, False otherwise
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists and not expired
        """
        return self.get(key) is not None

    def keys(self, pattern: str = "*") -> List[str]:
        """
        Get all keys matching pattern (simple * wildcard support).

        Args:
            pattern: Pattern to match (e.g., "user:*")

        Returns:
            List of matching keys
        """
        with self._lock:
            # Clean up expired entries
            expired_keys = [k for k, v in self._cache.items() if v.is_expired()]
            for k in expired_keys:
                del self._cache[k]

            if pattern == "*":
                return list(self._cache.keys())

            # Simple pattern matching
            if pattern.endswith("*"):
                prefix = pattern[:-1]
                return [k for k in self._cache.keys() if k.startswith(prefix)]
            elif pattern.startswith("*"):
                suffix = pattern[1:]
                return [k for k in self._cache.keys() if k.endswith(suffix)]
            else:
                return [k for k in self._cache.keys() if k == pattern]

    def incr(self, key: str, amount: int = 1) -> int:
        """
        Increment a numeric value.

        Args:
            key: Cache key
            amount: Amount to increment by

        Returns:
            New value after increment
        """
        with self._lock:
            current = self.get(key, deserialize=False)
            if current is None:
                new_value = amount
            else:
                try:
                    new_value = int(current) + amount
                except (ValueError, TypeError):
                    new_value = amount

            self.set(key, str(new_value), serialize=False)
            return new_value

    def decr(self, key: str, amount: int = 1) -> int:
        """
        Decrement a numeric value.

        Args:
            key: Cache key
            amount: Amount to decrement by

        Returns:
            New value after decrement
        """
        return self.incr(key, -amount)

    def expire(self, key: str, ttl: int) -> bool:
        """
        Set TTL on an existing key.

        Args:
            key: Cache key
            ttl: Time to live in seconds

        Returns:
            True if key exists, False otherwise
        """
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return False

            entry.expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
            return True

    def ttl(self, key: str) -> Optional[int]:
        """
        Get remaining TTL for a key.

        Args:
            key: Cache key

        Returns:
            TTL in seconds, None if no expiration, -1 if key doesn't exist
        """
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return -1

            if entry.expires_at is None:
                return None

            remaining = (entry.expires_at - datetime.now(timezone.utc)).total_seconds()
            return max(0, int(remaining))

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._pubsub_channels.clear()

    def info(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache info
        """
        with self._lock:
            # Clean up expired entries
            expired_keys = [k for k, v in self._cache.items() if v.is_expired()]
            for k in expired_keys:
                del self._cache[k]

            total_size = sum(
                len(str(entry.value)) for entry in self._cache.values()
            )

            return {
                "total_keys": len(self._cache),
                "total_size_bytes": total_size,
                "pubsub_channels": len(self._pubsub_channels),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    # Pub/Sub functionality for real-time updates
    def publish(self, channel: str, message: Any) -> int:
        """
        Publish message to a channel.

        Args:
            channel: Channel name
            message: Message to publish

        Returns:
            Number of subscribers that received the message
        """
        with self._lock:
            subscribers = self._pubsub_channels.get(channel, [])
            for callback in subscribers:
                try:
                    callback(channel, message)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")

            return len(subscribers)

    def subscribe(self, channel: str, callback: callable) -> None:
        """
        Subscribe to a channel.

        Args:
            channel: Channel name
            callback: Callback function(channel, message)
        """
        with self._lock:
            if channel not in self._pubsub_channels:
                self._pubsub_channels[channel] = []
            self._pubsub_channels[channel].append(callback)

    def unsubscribe(self, channel: str, callback: callable) -> None:
        """
        Unsubscribe from a channel.

        Args:
            channel: Channel name
            callback: Callback function to remove
        """
        with self._lock:
            if channel in self._pubsub_channels:
                try:
                    self._pubsub_channels[channel].remove(callback)
                    if not self._pubsub_channels[channel]:
                        del self._pubsub_channels[channel]
                except ValueError:
                    pass


# Global cache instance
_cache_instance: Optional[RedisEmulator] = None


def get_cache() -> RedisEmulator:
    """
    Get global cache instance (singleton).

    Returns:
        RedisEmulator instance
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisEmulator()
    return _cache_instance
