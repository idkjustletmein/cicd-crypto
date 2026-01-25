"""Additive Cipher implementation."""

from .base import BaseCipher


class AdditiveCipher(BaseCipher):
    """
    Additive Cipher - adds a fixed value to each letter position.
    E(x) = (x + k) mod 26
    D(y) = (y - k) mod 26
    """
    
    name = "Additive Cipher"
    description = (
        "The Additive cipher (also known as shift cipher) encrypts by adding a "
        "constant key value to each letter's position modulo 26. It's mathematically "
        "equivalent to Caesar cipher but expressed as modular addition."
    )
    key_type = "number"
    key_hint = "Enter additive key (0-25)"
    
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt using Additive cipher: E(x) = (x + k) mod 26"""
        k = int(key) % 26
        result = []
        
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                x = ord(char) - base
                encrypted = (x + k) % 26
                result.append(chr(encrypted + base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt using Additive cipher: D(y) = (y - k) mod 26"""
        k = int(key) % 26
        result = []
        
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                y = ord(char) - base
                decrypted = (y - k) % 26
                result.append(chr(decrypted + base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        try:
            k = int(key)
            if 0 <= k <= 25:
                return True, ""
            return False, "Key must be between 0 and 25"
        except (ValueError, TypeError):
            return False, "Key must be a number"
