"""Autokey Cipher implementation."""

from .base import BaseCipher


class AutokeyCipher(BaseCipher):
    """
    Autokey Cipher - uses the plaintext itself as part of the key.
    The key is primed with a keyword, then extended using the plaintext.
    """
    
    name = "Autokey Cipher"
    description = (
        "The Autokey cipher is a variant of Vigenère that uses the plaintext itself "
        "to extend the key. After the initial keyword is exhausted, the plaintext "
        "letters become the key. This eliminates the repeating key weakness."
    )
    key_type = "text"
    key_hint = "Enter primer keyword (letters only)"
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Autokey cipher."""
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError("Key must contain at least one letter")
        
        # Extract letters from plaintext for key extension
        plaintext_letters = ''.join(c.upper() for c in plaintext if c.isalpha())
        
        # Full key = primer key + plaintext (we only need as many as plaintext letters)
        full_key = key + plaintext_letters
        
        result = []
        key_index = 0
        
        for char in plaintext:
            if char.isalpha():
                x = ord(char.upper()) - ord('A')
                shift = ord(full_key[key_index]) - ord('A')
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
        """Decrypt using Autokey cipher."""
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError("Key must contain at least one letter")
        
        result = []
        current_key = list(key)
        key_index = 0
        
        for char in ciphertext:
            if char.isalpha():
                y = ord(char.upper()) - ord('A')
                shift = ord(current_key[key_index]) - ord('A')
                decrypted = (y - shift) % 26
                
                decrypted_char = chr(decrypted + ord('A'))
                
                if char.isupper():
                    result.append(decrypted_char)
                else:
                    result.append(decrypted_char.lower())
                
                # Extend key with decrypted plaintext letter
                current_key.append(decrypted_char)
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
            return False, "Key must contain at least one letter"
        return True, ""
