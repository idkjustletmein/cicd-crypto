"""Vigenère Cipher implementation."""

from .base import BaseCipher


class VigenereCipher(BaseCipher):
    """
    Vigenère Cipher - polyalphabetic substitution using a keyword.
    """
    
    name = "Vigenère Cipher"
    description = (
        "The Vigenère cipher uses a keyword to shift letters by varying amounts. "
        "Each letter of the key determines the shift for the corresponding plaintext "
        "letter. It was considered unbreakable for 300 years until Kasiski's method "
        "was discovered in 1863."
    )
    key_type = "text"
    key_hint = "Enter keyword (letters only)"
    strength = 4
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Vigenère cipher."""
        key = key.upper().replace(" ", "")
        result = []
        key_index = 0
        
        for char in plaintext.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                encrypted = (ord(char) - ord('A') + shift) % 26
                result.append(chr(encrypted + ord('A')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Vigenère cipher."""
        key = key.upper().replace(" ", "")
        result = []
        key_index = 0
        
        for char in ciphertext.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
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
            'key': 'KEY',
            'steps': [
                'H + K (shift 10) = R',
                'E + E (shift 4) = I',
                'L + Y (shift 24) = J',
                'L + K (shift 10) = V',
                'O + E (shift 4) = S',
            ],
            'result': 'RIJVS'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if not key.replace(" ", "").isalpha():
            return False, "Key must contain only letters"
        return True, ""
