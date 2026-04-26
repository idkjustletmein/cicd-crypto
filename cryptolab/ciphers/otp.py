"""One-Time Pad Cipher implementation."""

from .base import BaseCipher

KEY_ERROR_MSG = "Key must contain at least one letter"

class OTPCipher(BaseCipher):
    """
    One-Time Pad - theoretically unbreakable when used correctly.
    Key must be truly random, at least as long as message, and never reused.
    """
    
    name = "One-Time Pad"
    description = (
        "The One-Time Pad is the only cipher proven to be theoretically unbreakable "
        "when used correctly. The key must be truly random, at least as long as the "
        "message, and never reused. Each key letter shifts the corresponding plaintext."
    )
    key_type = "text"
    key_hint = "Enter key (must be at least as long as message letters)"
    
    def _process(self, text: str, key: str, is_encrypt: bool) -> str:
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError(KEY_ERROR_MSG)
        
        # Count letters in text
        letter_count = sum(1 for c in text if c.isalpha())
        if len(key) < letter_count:
            raise ValueError(f"Key ({len(key)} letters) must be at least as long as message ({letter_count} letters)")
        
        result = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                val = ord(char.upper()) - ord('A')
                shift = ord(key[key_index]) - ord('A')
                
                if is_encrypt:
                    new_val = (val + shift) % 26
                else:
                    new_val = (val - shift) % 26
                
                result.append(chr(new_val + base))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)

    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using One-Time Pad."""
        return self._process(plaintext, key, is_encrypt=True)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using One-Time Pad."""
        return self._process(ciphertext, key, is_encrypt=False)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        clean_key = ''.join(c for c in key if c.isalpha())
        if not clean_key:
            return False, KEY_ERROR_MSG
        return True, ""
