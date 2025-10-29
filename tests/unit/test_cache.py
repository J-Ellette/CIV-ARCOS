"""Tests for the Redis emulator cache layer."""

import time
import pytest
from civ_arcos.core.cache import RedisEmulator, get_cache


def test_cache_set_get():
    """Test basic set and get operations."""
    cache = RedisEmulator()
    
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"


def test_cache_set_get_with_serialization():
    """Test set and get with automatic JSON serialization."""
    cache = RedisEmulator()
    
    data = {"name": "test", "value": 123}
    cache.set("key1", data)
    result = cache.get("key1")
    
    assert result == data
    assert result["name"] == "test"
    assert result["value"] == 123


def test_cache_ttl():
    """Test TTL (time to live) functionality."""
    cache = RedisEmulator()
    
    # Set with 1 second TTL
    cache.set("key1", "value1", ttl=1)
    assert cache.get("key1") == "value1"
    
    # Wait for expiration
    time.sleep(1.1)
    assert cache.get("key1") is None


def test_cache_exists():
    """Test key existence check."""
    cache = RedisEmulator()
    
    assert not cache.exists("key1")
    cache.set("key1", "value1")
    assert cache.exists("key1")
    cache.delete("key1")
    assert not cache.exists("key1")


def test_cache_delete():
    """Test key deletion."""
    cache = RedisEmulator()
    
    cache.set("key1", "value1")
    assert cache.exists("key1")
    
    result = cache.delete("key1")
    assert result is True
    assert not cache.exists("key1")
    
    # Deleting non-existent key
    result = cache.delete("key1")
    assert result is False


def test_cache_keys_pattern():
    """Test keys with pattern matching."""
    cache = RedisEmulator()
    
    cache.set("user:1", "John")
    cache.set("user:2", "Jane")
    cache.set("post:1", "Hello")
    
    # Get all keys
    all_keys = cache.keys("*")
    assert len(all_keys) == 3
    
    # Get user keys
    user_keys = cache.keys("user:*")
    assert len(user_keys) == 2
    assert "user:1" in user_keys
    assert "user:2" in user_keys


def test_cache_incr_decr():
    """Test increment and decrement operations."""
    cache = RedisEmulator()
    
    # Increment from 0
    result = cache.incr("counter")
    assert result == 1
    
    result = cache.incr("counter", amount=5)
    assert result == 6
    
    # Decrement
    result = cache.decr("counter", amount=2)
    assert result == 4


def test_cache_expire():
    """Test setting expiration on existing key."""
    cache = RedisEmulator()
    
    cache.set("key1", "value1")
    assert cache.ttl("key1") is None  # No expiration
    
    cache.expire("key1", 2)
    ttl = cache.ttl("key1")
    assert ttl is not None
    assert ttl <= 2


def test_cache_ttl_remaining():
    """Test getting remaining TTL."""
    cache = RedisEmulator()
    
    # Non-existent key
    assert cache.ttl("nonexistent") == -1
    
    # Key without expiration
    cache.set("key1", "value1")
    assert cache.ttl("key1") is None
    
    # Key with expiration
    cache.set("key2", "value2", ttl=10)
    ttl = cache.ttl("key2")
    assert ttl > 0
    assert ttl <= 10


def test_cache_clear():
    """Test clearing all cache entries."""
    cache = RedisEmulator()
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    assert len(cache.keys("*")) == 3
    
    cache.clear()
    assert len(cache.keys("*")) == 0


def test_cache_info():
    """Test cache statistics."""
    cache = RedisEmulator()
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    info = cache.info()
    assert info["total_keys"] == 2
    assert "total_size_bytes" in info
    assert "timestamp" in info


def test_cache_pubsub():
    """Test pub/sub functionality."""
    cache = RedisEmulator()
    
    messages_received = []
    
    def callback(channel, message):
        messages_received.append((channel, message))
    
    # Subscribe to channel
    cache.subscribe("events", callback)
    
    # Publish message
    subscriber_count = cache.publish("events", {"type": "test", "data": "hello"})
    assert subscriber_count == 1
    
    # Check message received
    assert len(messages_received) == 1
    channel, message = messages_received[0]
    assert channel == "events"
    assert message["type"] == "test"


def test_cache_multiple_subscribers():
    """Test pub/sub with multiple subscribers."""
    cache = RedisEmulator()
    
    messages1 = []
    messages2 = []
    
    def callback1(channel, message):
        messages1.append(message)
    
    def callback2(channel, message):
        messages2.append(message)
    
    cache.subscribe("events", callback1)
    cache.subscribe("events", callback2)
    
    subscriber_count = cache.publish("events", "test message")
    assert subscriber_count == 2
    
    assert len(messages1) == 1
    assert len(messages2) == 1


def test_cache_unsubscribe():
    """Test unsubscribing from channels."""
    cache = RedisEmulator()
    
    messages = []
    
    def callback(channel, message):
        messages.append(message)
    
    cache.subscribe("events", callback)
    cache.publish("events", "message1")
    assert len(messages) == 1
    
    cache.unsubscribe("events", callback)
    cache.publish("events", "message2")
    assert len(messages) == 1  # No new message


def test_get_cache_singleton():
    """Test global cache singleton."""
    cache1 = get_cache()
    cache2 = get_cache()
    
    assert cache1 is cache2
    
    # Set in one, get in other
    cache1.set("key1", "value1")
    assert cache2.get("key1") == "value1"


def test_cache_thread_safety():
    """Test thread safety of cache operations."""
    import threading
    
    cache = RedisEmulator()
    errors = []
    
    def increment_counter():
        try:
            for _ in range(100):
                cache.incr("counter")
        except Exception as e:
            errors.append(e)
    
    # Create multiple threads
    threads = [threading.Thread(target=increment_counter) for _ in range(10)]
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    # Check no errors and correct final count
    assert len(errors) == 0
    assert cache.get("counter", deserialize=False) == "1000"


def test_cache_no_serialize():
    """Test cache with serialization disabled."""
    cache = RedisEmulator()
    
    cache.set("key1", "plain text", serialize=False)
    result = cache.get("key1", deserialize=False)
    assert result == "plain text"
    assert isinstance(result, str)
