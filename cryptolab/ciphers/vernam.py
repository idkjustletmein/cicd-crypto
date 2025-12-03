"""Vernam Cipher implementation."""

from .base import BaseCipher


class VernamCipher(BaseCipher):
    """
    Vernam Cipher - XOR-based binary encryption.
    """
    
    name = "Vernam Cipher"
    description = (
        "The Vernam cipher, invented by Gilbert Vernam in 1917, uses XOR operation "
        "between plaintext and key bits. When used with a truly random, never-reused "
        "key of the same length as the message, it becomes a One-Time Pad. It was "
        "used for teleprinter encryption."
    )
    key_type = "text"
    key_hint = "Enter key (letters, will be converted to binary)"
    strength = 8
    
    def _text_to_binary(self, text: str) -> str:
        """Convert text to binary string."""
        return ''.join(format(ord(c), '08b') for c in text)
    
    def _binary_to_text(self, binary: str) -> str:
        """Convert binary string to text."""
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)
    
    def _xor_strings(self, str1: str, str2: str) -> str:
        """XOR two binary strings."""
        return ''.join('1' if a != b else '0' for a, b in zip(str1, str2))
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Vernam cipher."""
        # Extend or truncate key to match plaintext length
        key_extended = (key * ((len(plaintext) // len(key)) + 1))[:len(plaintext)]
        
        plain_binary = self._text_to_binary(plaintext)
        key_binary = self._text_to_binary(key_extended)
        
        encrypted_binary = self._xor_strings(plain_binary, key_binary)
        
        # Return as hex for readability
        result = []
        for i in range(0, len(encrypted_binary), 8):
            byte = encrypted_binary[i:i+8]
            if len(byte) == 8:
                result.append(format(int(byte, 2), '02X'))
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Vernam cipher."""
        # Convert hex to binary
        cipher_binary = ''.join(format(int(ciphertext[i:i+2], 16), '08b') 
                                for i in range(0, len(ciphertext), 2))
        
        # Calculate needed key length
        key_length = len(cipher_binary) // 8
        key_extended = (key * ((key_length // len(key)) + 1))[:key_length]
        key_binary = self._text_to_binary(key_extended)
        
        decrypted_binary = self._xor_strings(cipher_binary, key_binary)
        
        return self._binary_to_text(decrypted_binary)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HI',
            'key': 'K',
            'steps': [
                'H = 01001000, I = 01001001',
                'K = 01001011 (repeated for each char)',
                'H XOR K: 01001000 XOR 01001011 = 00000011 → 03',
                'I XOR K: 01001001 XOR 01001011 = 00000010 → 02',
            ],
            'result': '0302'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if len(key) < 1:
            return False, "Key must have at least one character"
        return True, ""
