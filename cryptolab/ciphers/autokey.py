"""Autokey Cipher implementation."""

from .base import BaseCipher


class AutokeyCipher(BaseCipher):
    """
    Autokey Cipher - uses the plaintext itself as part of the key.
    """
    
    name = "Autokey Cipher"
    description = (
        "The Autokey cipher is a variant of Vigenère that uses the plaintext itself "
        "to extend the key. After the initial keyword is exhausted, the plaintext "
        "letters become the key. This eliminates the repeating key weakness of "
        "standard Vigenère."
    )
    key_type = "text"
    key_hint = "Enter primer keyword"
    strength = 5
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Autokey cipher."""
        key = key.upper().replace(" ", "")
        plaintext_clean = ''.join(c for c in plaintext.upper() if c.isalpha())
        full_key = key + plaintext_clean
        
        result = []
        key_index = 0
        
        for char in plaintext.upper():
            if char.isalpha():
                shift = ord(full_key[key_index]) - ord('A')
                encrypted = (ord(char) - ord('A') + shift) % 26
                result.append(chr(encrypted + ord('A')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Autokey cipher."""
        key = key.upper().replace(" ", "")
        result = []
        current_key = list(key)
        key_index = 0
        
        for char in ciphertext.upper():
            if char.isalpha():
                shift = ord(current_key[key_index]) - ord('A')
                decrypted = (ord(char) - ord('A') - shift) % 26
                decrypted_char = chr(decrypted + ord('A'))
                result.append(decrypted_char)
                current_key.append(decrypted_char)
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO',
            'key': 'KEY',
            'steps': [
                'Key extends: KEY + HELLO = KEYHEL...',
                'H + K (shift 10) = R',
                'E + E (shift 4) = I',
                'L + Y (shift 24) = J',
                'L + H (shift 7) = S',
                'O + E (shift 4) = S',
            ],
            'result': 'RIJSS'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if not key.replace(" ", "").isalpha():
            return False, "Key must contain only letters"
        return True, ""
