"""Vigenère Cipher implementation."""

from .base import BaseCipher

KEY_ERROR_MSG = "Key must contain at least one letter"

class VigenereCipher(BaseCipher):
    """
    Vigenère Cipher - polyalphabetic substitution using a keyword.
    Each letter of the key determines the shift for corresponding plaintext letter.
    """
    
    name = "Vigenère Cipher"
    description = (
        "The Vigenère cipher uses a keyword to shift letters by varying amounts. "
        "Each letter of the key determines the shift for the corresponding plaintext "
        "letter. It was considered unbreakable for 300 years."
    )
    key_type = "text"
    key_hint = "Enter keyword (letters only)"
    
    def _process(self, text: str, key: str, is_encrypt: bool) -> str:
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError(KEY_ERROR_MSG)
        
        result = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                val = ord(char.upper()) - ord('A')
                shift = ord(key[key_index % len(key)]) - ord('A')
                
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
        """Encrypt using Vigenère cipher."""
        return self._process(plaintext, key, is_encrypt=True)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Vigenère cipher."""
        return self._process(ciphertext, key, is_encrypt=False)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        clean_key = ''.join(c for c in key if c.isalpha())
        if not clean_key:
            return False, KEY_ERROR_MSG
        return True, ""
