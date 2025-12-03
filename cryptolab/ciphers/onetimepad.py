"""One-Time Pad Cipher implementation."""

from .base import BaseCipher


class OneTimePadCipher(BaseCipher):
    """
    One-Time Pad - theoretically unbreakable when used correctly.
    """
    
    name = "One-Time Pad"
    description = (
        "The One-Time Pad is the only cipher proven to be theoretically unbreakable "
        "when used correctly. The key must be truly random, at least as long as the "
        "message, never reused, and kept secret. In practice, key distribution makes "
        "it impractical for most uses."
    )
    key_type = "text"
    key_hint = "Enter key (must be as long as message)"
    strength = 10
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using One-Time Pad."""
        key = key.upper().replace(" ", "")
        result = []
        key_index = 0
        
        for char in plaintext.upper():
            if char.isalpha():
                if key_index >= len(key):
                    raise ValueError("Key must be at least as long as the message")
                shift = ord(key[key_index]) - ord('A')
                encrypted = (ord(char) - ord('A') + shift) % 26
                result.append(chr(encrypted + ord('A')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using One-Time Pad."""
        key = key.upper().replace(" ", "")
        result = []
        key_index = 0
        
        for char in ciphertext.upper():
            if char.isalpha():
                if key_index >= len(key):
                    raise ValueError("Key must be at least as long as the message")
                shift = ord(key[key_index]) - ord('A')
                decrypted = (ord(char) - ord('A') - shift) % 26
                result.append(chr(decrypted + ord('A')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO',
            'key': 'XMCKL',
            'steps': [
                'H (7) + X (23) mod 26 = E (4)',
                'E (4) + M (12) mod 26 = Q (16)',
                'L (11) + C (2) mod 26 = N (13)',
                'L (11) + K (10) mod 26 = V (21)',
                'O (14) + L (11) mod 26 = Z (25)',
            ],
            'result': 'EQNVZ'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if not key.replace(" ", "").isalpha():
            return False, "Key must contain only letters"
        return True, ""
