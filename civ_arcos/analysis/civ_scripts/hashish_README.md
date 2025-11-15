# Hashish - Cryptographic Hash Generator

Cryptographic hash generator for Python development using hashlib.

## Description

Hashish provides functionality for generating cryptographic hashes for data integrity verification and fingerprinting.

## Usage

```python
from civ_arcos.analysis.civ_scripts.hashish import Hashish

hasher = Hashish()

# Generate hash
sha256_hash = hasher.hash("data to hash")
print(f"SHA256: {sha256_hash}")

# Use convenience methods
md5_hash = hasher.md5("data")
sha1_hash = hasher.sha1("data")
sha256_hash = hasher.sha256("data")
sha512_hash = hasher.sha512("data")

# Hash a file
file_hash = hasher.hash_file("document.pdf", algorithm="sha256")

# Verify hash
is_valid = hasher.verify("data", expected_hash="abc123...")

# List available algorithms
algorithms = hasher.available_algorithms()
```

## Features

- Multiple hash algorithms (MD5, SHA1, SHA256, SHA384, SHA512, SHA3, BLAKE2)
- File hashing with chunked reading
- Hash verification
- Incremental hashing with hash objects
- Statistics tracking
- Support for all hashlib algorithms

## API Reference

### Constructor

- `Hashish()` - Initialize hash generator

### Hashing Methods

- `hash(data, algorithm='sha256')` - Generate hash with specified algorithm
- `md5(data)` - Generate MD5 hash
- `sha1(data)` - Generate SHA1 hash
- `sha256(data)` - Generate SHA256 hash
- `sha384(data)` - Generate SHA384 hash
- `sha512(data)` - Generate SHA512 hash
- `sha3_256(data)` - Generate SHA3-256 hash
- `sha3_512(data)` - Generate SHA3-512 hash
- `blake2b(data, digest_size=64)` - Generate BLAKE2b hash
- `blake2s(data, digest_size=32)` - Generate BLAKE2s hash

### File Methods

- `hash_file(filepath, algorithm='sha256', chunk_size=8192)` - Hash file contents

### Verification Methods

- `verify(data, expected_hash, algorithm='sha256')` - Verify data matches expected hash

### Advanced Methods

- `new(algorithm)` - Create new hash object for incremental hashing
- `available_algorithms()` - Get list of available hash algorithms

### Statistics Methods

- `get_results()` - Get processing results
- `get_statistics()` - Get detailed statistics

## Examples

### Basic Hashing

```python
hasher = Hashish()
hash_value = hasher.sha256("Hello, World!")
print(f"Hash: {hash_value}")
```

### File Hashing

```python
# Hash a file
hasher = Hashish()
file_hash = hasher.hash_file("largefile.bin", algorithm="sha512")
print(f"File SHA512: {file_hash}")
```

### Hash Verification

```python
hasher = Hashish()
data = "important data"
hash_value = hasher.sha256(data)

# Later, verify integrity
is_valid = hasher.verify(data, hash_value, algorithm="sha256")
print(f"Data integrity: {'OK' if is_valid else 'CORRUPTED'}")
```

### Incremental Hashing

```python
hasher = Hashish()
h = hasher.new("sha256")
h.update("Part 1")
h.update("Part 2")
h.update("Part 3")
final_hash = h.hexdigest()
```

### BLAKE2 Hashing

```python
# BLAKE2b with custom digest size
hasher = Hashish()
hash_value = hasher.blake2b("data", digest_size=32)

# BLAKE2s
hash_value = hasher.blake2s("data", digest_size=16)
```

### Statistics

```python
hasher = Hashish()
hasher.sha256("data1")
hasher.sha512("data2")
hasher.md5("data3")

stats = hasher.get_statistics()
# {'total_hashes': 3, 'unique_algorithms': 3,
#  'algorithms_used': {'sha256': 1, 'sha512': 1, 'md5': 1}}
```

## Supported Algorithms

### Standard Algorithms
- **MD5**: Fast but cryptographically broken (avoid for security)
- **SHA1**: Fast but deprecated for security (avoid for security)
- **SHA256**: Recommended for most uses
- **SHA384**: Longer SHA-2 variant
- **SHA512**: Most secure SHA-2 variant

### SHA-3 Algorithms
- **SHA3-224, SHA3-256, SHA3-384, SHA3-512**: Modern Keccak-based algorithms

### BLAKE2 Algorithms
- **BLAKE2b**: Optimized for 64-bit platforms
- **BLAKE2s**: Optimized for 32-bit platforms

## Security Notes

- SHA256 or SHA512 recommended for security-critical applications
- MD5 and SHA1 should only be used for non-security purposes
- Use BLAKE2 for high-performance hashing
- File hashing uses chunked reading to handle large files efficiently

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.hashish
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
