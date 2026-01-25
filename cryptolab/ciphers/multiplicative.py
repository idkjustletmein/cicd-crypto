"""Multiplicative Cipher implementation."""

from math import gcd
from .base import BaseCipher


class MultiplicativeCipher(BaseCipher):
    """
    Multiplicative Cipher - multiplies each letter position by a key.
    E(x) = (x * k) mod 26
    D(y) = (y * k^-1) mod 26
    """
    
    name = "Multiplicative Cipher"
    description = (
        "The Multiplicative cipher encrypts by multiplying each letter's position "
        "by a key value modulo 26. The key must be coprime with 26 (valid keys: "
        "1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25) to allow decryption."
    )
    key_type = "number"
    key_hint = "Enter multiplier (coprime with 26: 1,3,5,7,9,11,15,17,19,21,23,25)"
    
    # Pre-computed modular inverses for valid keys mod 26
    MOD_INVERSES = {
        1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19,
        15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25
    }
    
    def _mod_inverse(self, a: int) -> int:
        """Get modular multiplicative inverse of a mod 26."""
        a = a % 26
        if a in self.MOD_INVERSES:
            return self.MOD_INVERSES[a]
        raise ValueError(f"No modular inverse for {a} mod 26")
    
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt using Multiplicative cipher: E(x) = (x * k) mod 26"""
        k = int(key) % 26
        result = []
        
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                x = ord(char) - base
                encrypted = (x * k) % 26
                result.append(chr(encrypted + base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt using Multiplicative cipher: D(y) = (y * k^-1) mod 26"""
        k = int(key) % 26
        k_inv = self._mod_inverse(k)
        result = []
        
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                y = ord(char) - base
                decrypted = (y * k_inv) % 26
                result.append(chr(decrypted + base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        try:
            k = int(key) % 26
            if gcd(k, 26) != 1:
                return False, f"Key must be coprime with 26. Valid: 1,3,5,7,9,11,15,17,19,21,23,25"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be a number"
