"""One-Time Pad Cipher implementation."""

from .base import BaseCipher


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
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using One-Time Pad."""
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError("Key must contain at least one letter")
        
        # Count letters in plaintext
        letter_count = sum(1 for c in plaintext if c.isalpha())
        if len(key) < letter_count:
            raise ValueError(f"Key ({len(key)} letters) must be at least as long as message ({letter_count} letters)")
        
        result = []
        key_index = 0
        
        for char in plaintext:
            if char.isalpha():
                x = ord(char.upper()) - ord('A')
                shift = ord(key[key_index]) - ord('A')
                encrypted = (x + shift) % 26
                
                if char.isupper():
                    result.append(chr(encrypted + ord('A')))
                else:
                    result.append(chr(encrypted + ord('a')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using One-Time Pad."""
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError("Key must contain at least one letter")
        
        letter_count = sum(1 for c in ciphertext if c.isalpha())
        if len(key) < letter_count:
            raise ValueError(f"Key ({len(key)} letters) must be at least as long as message ({letter_count} letters)")
        
        result = []
        key_index = 0
        
        for char in ciphertext:
            if char.isalpha():
                y = ord(char.upper()) - ord('A')
                shift = ord(key[key_index]) - ord('A')
                decrypted = (y - shift) % 26
                
                if char.isupper():
                    result.append(chr(decrypted + ord('A')))
                else:
                    result.append(chr(decrypted + ord('a')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        clean_key = ''.join(c for c in key if c.isalpha())
        if not clean_key:
            return False, "Key must contain letters"
        return True, ""
