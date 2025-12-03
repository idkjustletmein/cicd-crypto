"""Affine Cipher implementation."""

from math import gcd
from .base import BaseCipher


class AffineCipher(BaseCipher):
    """
    Affine Cipher - combines multiplicative and additive ciphers.
    """
    
    name = "Affine Cipher"
    description = (
        "The Affine cipher encrypts using the formula E(x) = (ax + b) mod 26, "
        "where 'a' and 'b' are the keys. The value 'a' must be coprime with 26 "
        "(valid values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25). It combines "
        "the multiplicative and Caesar ciphers."
    )
    key_type = "text"
    key_hint = "Enter 'a b' (e.g., '5 8') where a is coprime with 26"
    strength = 3
    
    def _mod_inverse(self, a: int, m: int = 26) -> int:
        """Find modular multiplicative inverse."""
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"No modular inverse for {a} mod {m}")
    
    def _parse_key(self, key: str) -> tuple[int, int]:
        """Parse key string into a and b values."""
        parts = key.split()
        if len(parts) != 2:
            raise ValueError("Key must be two numbers: 'a b'")
        return int(parts[0]), int(parts[1])
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Affine cipher."""
        a, b = self._parse_key(key)
        result = []
        
        for char in plaintext.upper():
            if char.isalpha():
                x = ord(char) - ord('A')
                encrypted = (a * x + b) % 26
                result.append(chr(encrypted + ord('A')))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Affine cipher."""
        a, b = self._parse_key(key)
        a_inv = self._mod_inverse(a)
        result = []
        
        for char in ciphertext.upper():
            if char.isalpha():
                y = ord(char) - ord('A')
                decrypted = (a_inv * (y - b)) % 26
                result.append(chr(decrypted + ord('A')))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO',
            'key': '5 8',
            'steps': [
                'E(x) = (5x + 8) mod 26',
                'H (7): (5×7 + 8) mod 26 = 43 mod 26 = 17 → R',
                'E (4): (5×4 + 8) mod 26 = 28 mod 26 = 2 → C',
                'L (11): (5×11 + 8) mod 26 = 63 mod 26 = 11 → L',
                'L (11): (5×11 + 8) mod 26 = 63 mod 26 = 11 → L',
                'O (14): (5×14 + 8) mod 26 = 78 mod 26 = 0 → A',
            ],
            'result': 'RCLLA'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        try:
            parts = key.split()
            if len(parts) != 2:
                return False, "Key must be two numbers: 'a b'"
            a, b = int(parts[0]), int(parts[1])
            if gcd(a, 26) != 1:
                return False, f"'a' ({a}) must be coprime with 26. Valid: 1,3,5,7,9,11,15,17,19,21,23,25"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be two space-separated numbers"
