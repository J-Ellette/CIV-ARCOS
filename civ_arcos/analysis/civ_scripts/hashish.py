"""Hashish - Hash generator

Crypto hasher for development tasks.
Wrapper around Python's hashlib module for cryptographic hashing.
"""

import hashlib
from typing import Any, Dict, List, Optional, Union


class HashishHasher:
    """A wrapper around a hashlib hash object"""
    
    def __init__(self, algorithm: str):
        """Initialize hasher with specified algorithm"""
        self.algorithm = algorithm
        self._hasher = hashlib.new(algorithm)
    
    def update(self, data: Union[str, bytes]):
        """Update hash with new data"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._hasher.update(data)
    
    def digest(self) -> bytes:
        """Get binary hash digest"""
        return self._hasher.digest()
    
    def hexdigest(self) -> str:
        """Get hexadecimal hash digest"""
        return self._hasher.hexdigest()
    
    def copy(self):
        """Create a copy of this hasher"""
        new_hasher = HashishHasher.__new__(HashishHasher)
        new_hasher.algorithm = self.algorithm
        new_hasher._hasher = self._hasher.copy()
        return new_hasher


class Hashish:
    """
    Hashish: Crypto hasher
    
    Provides utilities to generate cryptographic hashes.
    """
    
    # Available algorithms
    ALGORITHMS = {
        'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
        'blake2b', 'blake2s'
    }
    
    def __init__(self):
        """Initialize Hashish"""
        self.hash_count = 0
        self.algorithms_used = {}
    
    def hash(self, 
             data: Union[str, bytes], 
             algorithm: str = 'sha256') -> str:
        """
        Generate hash of data using specified algorithm.
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm to use (default: sha256)
            
        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        hasher = hashlib.new(algorithm)
        hasher.update(data)
        result = hasher.hexdigest()
        
        self.hash_count += 1
        self.algorithms_used[algorithm] = self.algorithms_used.get(algorithm, 0) + 1
        
        return result
    
    def md5(self, data: Union[str, bytes]) -> str:
        """Generate MD5 hash"""
        return self.hash(data, 'md5')
    
    def sha1(self, data: Union[str, bytes]) -> str:
        """Generate SHA1 hash"""
        return self.hash(data, 'sha1')
    
    def sha256(self, data: Union[str, bytes]) -> str:
        """Generate SHA256 hash"""
        return self.hash(data, 'sha256')
    
    def sha384(self, data: Union[str, bytes]) -> str:
        """Generate SHA384 hash"""
        return self.hash(data, 'sha384')
    
    def sha512(self, data: Union[str, bytes]) -> str:
        """Generate SHA512 hash"""
        return self.hash(data, 'sha512')
    
    def sha3_256(self, data: Union[str, bytes]) -> str:
        """Generate SHA3-256 hash"""
        return self.hash(data, 'sha3_256')
    
    def sha3_512(self, data: Union[str, bytes]) -> str:
        """Generate SHA3-512 hash"""
        return self.hash(data, 'sha3_512')
    
    def blake2b(self, data: Union[str, bytes], digest_size: int = 64) -> str:
        """Generate BLAKE2b hash"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        hasher = hashlib.blake2b(data, digest_size=digest_size)
        self.hash_count += 1
        self.algorithms_used['blake2b'] = self.algorithms_used.get('blake2b', 0) + 1
        return hasher.hexdigest()
    
    def blake2s(self, data: Union[str, bytes], digest_size: int = 32) -> str:
        """Generate BLAKE2s hash"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        hasher = hashlib.blake2s(data, digest_size=digest_size)
        self.hash_count += 1
        self.algorithms_used['blake2s'] = self.algorithms_used.get('blake2s', 0) + 1
        return hasher.hexdigest()
    
    def new(self, algorithm: str) -> HashishHasher:
        """
        Create a new hash object for incremental hashing.
        
        Args:
            algorithm: Hash algorithm to use
            
        Returns:
            HashishHasher object
        """
        return HashishHasher(algorithm)
    
    def hash_file(self, 
                  filepath: str, 
                  algorithm: str = 'sha256',
                  chunk_size: int = 8192) -> str:
        """
        Generate hash of a file.
        
        Args:
            filepath: Path to file
            algorithm: Hash algorithm to use
            chunk_size: Size of chunks to read
            
        Returns:
            Hexadecimal hash string
        """
        hasher = hashlib.new(algorithm)
        
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        
        self.hash_count += 1
        self.algorithms_used[algorithm] = self.algorithms_used.get(algorithm, 0) + 1
        
        return hasher.hexdigest()
    
    def verify(self, data: Union[str, bytes], expected_hash: str, algorithm: str = 'sha256') -> bool:
        """
        Verify data matches expected hash.
        
        Args:
            data: Data to verify
            expected_hash: Expected hash value
            algorithm: Hash algorithm used
            
        Returns:
            True if hash matches, False otherwise
        """
        actual_hash = self.hash(data, algorithm)
        return actual_hash.lower() == expected_hash.lower()
    
    def available_algorithms(self) -> List[str]:
        """Get list of available hash algorithms"""
        return sorted(hashlib.algorithms_available)
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'hashes_generated': self.hash_count,
            'algorithms_used': dict(self.algorithms_used)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        return {
            'total_hashes': self.hash_count,
            'unique_algorithms': len(self.algorithms_used),
            'algorithms_used': dict(self.algorithms_used)
        }
