"""Caesar Cipher implementation."""

from .base import BaseCipher


class CaesarCipher(BaseCipher):
    """
    Caesar Cipher - shifts each letter by a fixed number of positions.
    One of the oldest known encryption techniques, used by Julius Caesar.
    """
    
    name = "Caesar Cipher"
    description = (
        "The Caesar cipher shifts each letter in the plaintext by a fixed number "
        "of positions in the alphabet. Named after Julius Caesar who used it for "
        "military communications. With only 26 possible keys, it's easily broken "
        "by brute force."
    )
    key_type = "number"
    key_hint = "Enter shift value (1-25)"
    strength = 1
    
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt using Caesar cipher."""
        shift = int(key) % 26
        result = []
        
        for char in plaintext.upper():
            if char.isalpha():
                shifted = (ord(char) - ord('A') + shift) % 26
                result.append(chr(shifted + ord('A')))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt using Caesar cipher."""
        shift = int(key) % 26
        return self.encrypt(ciphertext, 26 - shift)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO',
            'key': '3',
            'steps': [
                'H (position 7) + 3 = K (position 10)',
                'E (position 4) + 3 = H (position 7)',
                'L (position 11) + 3 = O (position 14)',
                'L (position 11) + 3 = O (position 14)',
                'O (position 14) + 3 = R (position 17)',
            ],
            'result': 'KHOOR'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        try:
            k = int(key)
            if 1 <= k <= 25:
                return True, ""
            return False, "Shift must be between 1 and 25"
        except (ValueError, TypeError):
            return False, "Key must be a number"
