"""Caesar Cipher implementation."""

from .base import BaseCipher


class CaesarCipher(BaseCipher):
    """
    Caesar Cipher - shifts each letter by a fixed number of positions.
    """
    
    name = "Caesar Cipher"
    description = (
        "The Caesar cipher shifts each letter in the plaintext by a fixed number "
        "of positions in the alphabet. Named after Julius Caesar who used it for "
        "military communications."
    )
    key_type = "number"
    key_hint = "Enter shift value (1-25)"
    
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt using Caesar cipher."""
        shift = int(key) % 26
        result = []
        
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(shifted + base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt using Caesar cipher."""
        shift = int(key) % 26
        return self.encrypt(ciphertext, 26 - shift)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        try:
            k = int(key)
            if 1 <= k <= 25:
                return True, ""
            return False, "Shift must be between 1 and 25"
        except (ValueError, TypeError):
            return False, "Key must be a number"
