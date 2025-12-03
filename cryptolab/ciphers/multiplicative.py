"""Multiplicative Cipher implementation."""

from math import gcd
from .base import BaseCipher


class MultiplicativeCipher(BaseCipher):
    """
    Multiplicative Cipher - multiplies each letter position by a key.
    """
    
    name = "Multiplicative Cipher"
    description = (
        "The Multiplicative cipher encrypts by multiplying each letter's position "
        "by a key value modulo 26. The key must be coprime with 26 to allow "
        "decryption. It's a special case of the Affine cipher where b=0."
    )
    key_type = "number"
    key_hint = "Enter multiplier (coprime with 26: 1,3,5,7,9,11,15,17,19,21,23,25)"
    strength = 2
    
    def _mod_inverse(self, a: int, m: int = 26) -> int:
        """Find modular multiplicative inverse."""
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"No modular inverse for {a} mod {m}")
    
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt using Multiplicative cipher."""
        k = int(key)
        result = []
        
        for char in plaintext.upper():
            if char.isalpha():
                x = ord(char) - ord('A')
                encrypted = (k * x) % 26
                result.append(chr(encrypted + ord('A')))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt using Multiplicative cipher."""
        k = int(key)
        k_inv = self._mod_inverse(k)
        result = []
        
        for char in ciphertext.upper():
            if char.isalpha():
                y = ord(char) - ord('A')
                decrypted = (k_inv * y) % 26
                result.append(chr(decrypted + ord('A')))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO',
            'key': '7',
            'steps': [
                'E(x) = (7 × x) mod 26',
                'H (7): 7 × 7 mod 26 = 49 mod 26 = 23 → X',
                'E (4): 7 × 4 mod 26 = 28 mod 26 = 2 → C',
                'L (11): 7 × 11 mod 26 = 77 mod 26 = 25 → Z',
                'L (11): 7 × 11 mod 26 = 77 mod 26 = 25 → Z',
                'O (14): 7 × 14 mod 26 = 98 mod 26 = 20 → U',
            ],
            'result': 'XCZZU'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        try:
            k = int(key)
            if gcd(k, 26) != 1:
                return False, f"Key ({k}) must be coprime with 26. Valid: 1,3,5,7,9,11,15,17,19,21,23,25"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be a number"
