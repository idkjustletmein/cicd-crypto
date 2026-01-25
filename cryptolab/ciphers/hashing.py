"""Hashing implementations - MD5, SHA-1, SHA-256."""

import hashlib
from .base import BaseCipher


class HashingCipher(BaseCipher):
    """
    Cryptographic Hash Functions - one-way functions.
    Supports MD5, SHA-1, SHA-256, SHA-512.
    Note: Hashing is one-way, decryption returns explanation.
    """
    
    name = "Hashing"
    description = (
        "Cryptographic hash functions produce a fixed-size digest from any input. "
        "They are one-way functions - you cannot recover the original from the hash. "
        "Select algorithm: md5, sha1, sha256, sha512."
    )
    key_type = "text"
    key_hint = "Enter algorithm: md5, sha1, sha256, or sha512"
    
    SUPPORTED_ALGORITHMS = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Generate hash digest of the plaintext."""
        algorithm = str(key).lower().strip()
        
        if algorithm not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm}. Use: md5, sha1, sha256, sha512")
        
        hash_func = self.SUPPORTED_ALGORITHMS[algorithm]
        digest = hash_func(plaintext.encode('utf-8')).hexdigest()
        
        return digest.upper()
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Hashing is one-way - cannot decrypt.
        Returns explanation instead.
        """
        algorithm = str(key).lower().strip()
        
        return (
            f"Hash functions are ONE-WAY - decryption is not possible.\n"
            f"The {algorithm.upper()} hash '{ciphertext[:32]}...' cannot be reversed.\n"
            f"To verify, hash your candidate plaintext and compare digests."
        )
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Algorithm is required (md5, sha1, sha256, sha512)"
        
        algorithm = key.lower().strip()
        if algorithm not in cls.SUPPORTED_ALGORITHMS:
            return False, f"Unknown algorithm. Use: md5, sha1, sha256, sha512"
        return True, ""


class SHA1Cipher(BaseCipher):
    """
    SHA-1 Hash Function - dedicated SHA-1 hasher.
    """
    
    name = "SHA-1"
    description = (
        "SHA-1 (Secure Hash Algorithm 1) produces a 160-bit (20-byte) hash value. "
        "It was designed by the NSA. While now considered cryptographically broken "
        "for collision resistance, it's still widely used for non-security purposes."
    )
    key_type = "text"
    key_hint = "No key needed (enter anything)"
    
    def encrypt(self, plaintext: str, key: str = "") -> str:
        """Generate SHA-1 hash of the plaintext."""
        digest = hashlib.sha1(plaintext.encode('utf-8')).hexdigest()
        return digest.upper()
    
    def decrypt(self, ciphertext: str, key: str = "") -> str:
        """SHA-1 is one-way - cannot decrypt."""
        return (
            f"SHA-1 is a ONE-WAY hash function - decryption is impossible.\n"
            f"Hash: {ciphertext}\n"
            f"To verify data, hash it and compare with this digest."
        )
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        return True, ""  # No key needed for hashing
