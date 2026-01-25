"""Affine Cipher implementation."""

from math import gcd
from .base import BaseCipher


class AffineCipher(BaseCipher):
    """
    Affine Cipher - combines multiplicative and additive ciphers.
    E(x) = (a*x + b) mod 26
    D(y) = a^-1 * (y - b) mod 26
    """
    
    name = "Affine Cipher"
    description = (
        "The Affine cipher encrypts using E(x) = (ax + b) mod 26, where 'a' and 'b' "
        "are the keys. The value 'a' must be coprime with 26 (valid: 1,3,5,7,9,11,"
        "15,17,19,21,23,25). It combines multiplicative and additive ciphers."
    )
    key_type = "text"
    key_hint = "Enter 'a b' (e.g., '5 8') where a is coprime with 26"
    
    # Pre-computed modular inverses mod 26
    MOD_INVERSES = {
        1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19,
        15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25
    }
    
    def _parse_key(self, key: str) -> tuple:
        """Parse key string into a and b values."""
        parts = str(key).split()
        if len(parts) != 2:
            raise ValueError("Key must be two numbers: 'a b'")
        return int(parts[0]), int(parts[1])
    
    def _mod_inverse(self, a: int) -> int:
        """Get modular multiplicative inverse of a mod 26."""
        a = a % 26
        if a in self.MOD_INVERSES:
            return self.MOD_INVERSES[a]
        raise ValueError(f"No modular inverse for {a} mod 26")
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Affine cipher: E(x) = (a*x + b) mod 26"""
        a, b = self._parse_key(key)
        a = a % 26
        b = b % 26
        result = []
        
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                x = ord(char) - base
                encrypted = (a * x + b) % 26
                result.append(chr(encrypted + base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Affine cipher: D(y) = a^-1 * (y - b) mod 26"""
        a, b = self._parse_key(key)
        a = a % 26
        b = b % 26
        a_inv = self._mod_inverse(a)
        result = []
        
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                y = ord(char) - base
                decrypted = (a_inv * (y - b)) % 26
                result.append(chr(decrypted + base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        try:
            parts = str(key).split()
            if len(parts) != 2:
                return False, "Key must be two numbers: 'a b'"
            a, b = int(parts[0]), int(parts[1])
            if gcd(a % 26, 26) != 1:
                return False, f"'a' ({a}) must be coprime with 26. Valid: 1,3,5,7,9,11,15,17,19,21,23,25"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be two space-separated numbers"
