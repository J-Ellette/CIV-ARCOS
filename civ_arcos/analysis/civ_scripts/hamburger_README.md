# Hamburger - HMAC Signature Creator

HMAC signature creator for Python development using hmac.

## Description

Hamburger provides functionality for creating and verifying HMAC (Hash-based Message Authentication Code) signatures for message authentication.

## Usage

```python
from civ_arcos.analysis.civ_scripts.hamburger import Hamburger

burger = Hamburger(key="secret-key")

# Create signature
signature = burger.sign("message to sign")
print(f"Signature: {signature}")

# Verify signature
is_valid = burger.verify("message to sign", signature)
print(f"Valid: {is_valid}")

# Sign with different algorithms
sha256_sig = burger.sign_sha256("data")
sha512_sig = burger.sign_sha512("data")
sha1_sig = burger.sign_sha1("data")

# Webhook signatures
webhook_sig = burger.sign_webhook(payload='{"data": "value"}', secret="webhook-secret")
is_valid = burger.verify_webhook(
    payload='{"data": "value"}',
    signature_header=webhook_sig,
    secret="webhook-secret"
)
```

## Features

- HMAC signature creation
- Signature verification with constant-time comparison
- Multiple hash algorithms (SHA256, SHA512, SHA1, MD5)
- Webhook signature support
- Incremental signing with HMAC objects
- Statistics tracking

## API Reference

### Constructor

- `Hamburger(key=None)` - Initialize with optional default key

### Signing Methods

- `sign(message, key=None, algorithm='sha256')` - Create HMAC signature
- `sign_sha256(message, key=None)` - Create HMAC-SHA256 signature
- `sign_sha512(message, key=None)` - Create HMAC-SHA512 signature
- `sign_sha1(message, key=None)` - Create HMAC-SHA1 signature
- `sign_md5(message, key=None)` - Create HMAC-MD5 signature

### Verification Methods

- `verify(message, signature, key=None, algorithm='sha256')` - Verify HMAC signature
- `compare_digest(a, b)` - Constant-time digest comparison

### Webhook Methods

- `sign_webhook(payload, secret, algorithm='sha256')` - Sign webhook payload
- `verify_webhook(payload, signature_header, secret)` - Verify webhook signature

### Advanced Methods

- `new(key, message=None, algorithm='sha256')` - Create new HMAC object for incremental signing

### Statistics Methods

- `get_results()` - Get processing results
- `get_statistics()` - Get detailed statistics

## Examples

### Basic Signature

```python
burger = Hamburger(key="my-secret")
signature = burger.sign("Hello, World!")
is_valid = burger.verify("Hello, World!", signature)
```

### Webhook Verification

```python
# GitHub-style webhook
burger = Hamburger()
signature = burger.sign_webhook(
    payload='{"event": "push"}',
    secret="github-secret",
    algorithm="sha256"
)
# Returns: "sha256=<hex_signature>"

# Verify incoming webhook
is_valid = burger.verify_webhook(
    payload='{"event": "push"}',
    signature_header="sha256=abc123...",
    secret="github-secret"
)
```

### Incremental Signing

```python
burger = Hamburger()
h = burger.new(key="secret", message=b"Part 1")
h.update(b"Part 2")
h.update(b"Part 3")
signature = h.hexdigest()
```

### Statistics

```python
burger = Hamburger(key="secret")
burger.sign("message1")
burger.sign("message2")
burger.verify("message1", "invalid")
burger.verify("message2", burger.sign("message2"))

stats = burger.get_statistics()
# {'total_signatures': 3, 'total_verifications': 2, 
#  'verification_success_rate': 0.5, ...}
```

## Security Notes

- Uses constant-time comparison (`hmac.compare_digest`) to prevent timing attacks
- Supports modern hash algorithms (SHA256, SHA512, SHA3)
- Follows best practices for HMAC implementation

## Testing

```bash
python -m civ_arcos.analysis.civ_scripts.hamburger
```

## License

Part of the Emu-Soft project - see main repository LICENSE.
