"""Hamburger - HMAC generator

Signature creator for development tasks.
Wrapper around Python's hmac module for message authentication.
"""

import hmac
import hashlib
from typing import Any, Dict, List, Union


class Hamburger:
    """
    Hamburger: Signature creator
    
    Provides utilities to create and verify HMAC signatures.
    """
    
    def __init__(self, key: Union[str, bytes, None] = None):
        """
        Initialize Hamburger.
        
        Args:
            key: Default secret key for HMAC operations (optional)
        """
        if key and isinstance(key, str):
            key = key.encode('utf-8')
        self.default_key = key
        self.signature_count = 0
        self.verifications = {'passed': 0, 'failed': 0}
    
    def sign(self, 
             message: Union[str, bytes], 
             key: Union[str, bytes, None] = None,
             algorithm: str = 'sha256') -> str:
        """
        Create HMAC signature for a message.
        
        Args:
            message: Message to sign
            key: Secret key (uses default if not provided)
            algorithm: Hash algorithm to use (default: sha256)
            
        Returns:
            Hexadecimal HMAC signature
        """
        # Use provided key or default key
        if key is None:
            key = self.default_key
        
        if key is None:
            raise ValueError("No key provided and no default key set")
        
        # Convert to bytes if needed
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        # Get the digest method
        digestmod = getattr(hashlib, algorithm)
        
        # Create HMAC
        signature = hmac.new(key, message, digestmod).hexdigest()
        self.signature_count += 1
        
        return signature
    
    def verify(self, 
               message: Union[str, bytes], 
               signature: str,
               key: Union[str, bytes, None] = None,
               algorithm: str = 'sha256') -> bool:
        """
        Verify HMAC signature for a message.
        
        Args:
            message: Message to verify
            signature: Expected signature
            key: Secret key (uses default if not provided)
            algorithm: Hash algorithm used
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            expected_signature = self.sign(message, key, algorithm)
            # Use constant-time comparison to prevent timing attacks
            result = hmac.compare_digest(expected_signature, signature)
            
            if result:
                self.verifications['passed'] += 1
            else:
                self.verifications['failed'] += 1
            
            return result
        except Exception:
            self.verifications['failed'] += 1
            return False
    
    def sign_sha256(self, message: Union[str, bytes], key: Union[str, bytes, None] = None) -> str:
        """Create HMAC-SHA256 signature"""
        return self.sign(message, key, 'sha256')
    
    def sign_sha1(self, message: Union[str, bytes], key: Union[str, bytes, None] = None) -> str:
        """Create HMAC-SHA1 signature"""
        return self.sign(message, key, 'sha1')
    
    def sign_sha512(self, message: Union[str, bytes], key: Union[str, bytes, None] = None) -> str:
        """Create HMAC-SHA512 signature"""
        return self.sign(message, key, 'sha512')
    
    def sign_md5(self, message: Union[str, bytes], key: Union[str, bytes, None] = None) -> str:
        """Create HMAC-MD5 signature"""
        return self.sign(message, key, 'md5')
    
    def new(self, 
            key: Union[str, bytes], 
            message: Union[str, bytes, None] = None,
            algorithm: str = 'sha256') -> hmac.HMAC:
        """
        Create a new HMAC object for incremental signing.
        
        Args:
            key: Secret key
            message: Initial message (optional)
            algorithm: Hash algorithm to use
            
        Returns:
            HMAC object
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        if message and isinstance(message, str):
            message = message.encode('utf-8')
        
        digestmod = getattr(hashlib, algorithm)
        return hmac.new(key, message, digestmod)
    
    def compare_digest(self, a: Union[str, bytes], b: Union[str, bytes]) -> bool:
        """
        Constant-time comparison of two digests.
        
        Args:
            a: First digest
            b: Second digest
            
        Returns:
            True if digests match, False otherwise
        """
        return hmac.compare_digest(a, b)
    
    def sign_webhook(self, 
                     payload: Union[str, bytes], 
                     secret: Union[str, bytes],
                     algorithm: str = 'sha256') -> str:
        """
        Sign a webhook payload (common use case).
        
        Args:
            payload: Webhook payload
            secret: Webhook secret
            algorithm: Hash algorithm
            
        Returns:
            Signature in format 'algorithm=signature'
        """
        signature = self.sign(payload, secret, algorithm)
        return f"{algorithm}={signature}"
    
    def verify_webhook(self,
                       payload: Union[str, bytes],
                       signature_header: str,
                       secret: Union[str, bytes]) -> bool:
        """
        Verify a webhook signature.
        
        Args:
            payload: Webhook payload
            signature_header: Signature from header (e.g., 'sha256=...')
            secret: Webhook secret
            
        Returns:
            True if signature is valid, False otherwise
        """
        # Parse algorithm and signature from header
        if '=' in signature_header:
            algorithm, signature = signature_header.split('=', 1)
        else:
            algorithm = 'sha256'
            signature = signature_header
        
        return self.verify(payload, signature, secret, algorithm)
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'signatures_created': self.signature_count,
            'verifications': dict(self.verifications)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        total_verifications = self.verifications['passed'] + self.verifications['failed']
        
        return {
            'total_signatures': self.signature_count,
            'total_verifications': total_verifications,
            'verification_success_rate': (
                self.verifications['passed'] / total_verifications 
                if total_verifications > 0 else 0
            ),
            'passed_verifications': self.verifications['passed'],
            'failed_verifications': self.verifications['failed']
        }
