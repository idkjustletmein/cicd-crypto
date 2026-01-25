"""Vernam Cipher implementation."""

from .base import BaseCipher


class VernamCipher(BaseCipher):
    """
    Vernam Cipher - XOR-based binary encryption.
    Uses XOR operation between plaintext and key bits.
    """
    
    name = "Vernam Cipher"
    description = (
        "The Vernam cipher, invented by Gilbert Vernam in 1917, uses XOR operation "
        "between plaintext and key. Each character is XORed with the corresponding "
        "key character. The key repeats if shorter than the message. Output is hex."
    )
    key_type = "text"
    key_hint = "Enter key (any characters)"
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Vernam cipher (XOR). Returns hex string."""
        key = str(key)
        if not key:
            raise ValueError("Key is required")
        
        result = []
        for i, char in enumerate(plaintext):
            key_char = key[i % len(key)]
            xor_result = ord(char) ^ ord(key_char)
            result.append(format(xor_result, '02X'))
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Vernam cipher. Input is hex string."""
        key = str(key)
        if not key:
            raise ValueError("Key is required")
        
        # Remove any spaces from hex string
        ciphertext = ciphertext.replace(' ', '')
        
        result = []
        key_index = 0
        
        for i in range(0, len(ciphertext), 2):
            hex_byte = ciphertext[i:i+2]
            if len(hex_byte) < 2:
                break
            
            byte_value = int(hex_byte, 16)
            key_char = key[key_index % len(key)]
            xor_result = byte_value ^ ord(key_char)
            result.append(chr(xor_result))
            key_index += 1
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if len(key) < 1:
            return False, "Key must have at least one character"
        return True, ""
