"""DES Cipher implementation using PyCryptodome."""

import base64
from .base import BaseCipher

try:
    from Crypto.Cipher import DES
    from Crypto.Util.Padding import pad, unpad
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class DESCipher(BaseCipher):
    """
    DES (Data Encryption Standard) - symmetric block cipher.
    Uses 56-bit key (8 bytes with parity) and 64-bit blocks.
    """
    
    name = "DES"
    description = (
        "DES (Data Encryption Standard) is a symmetric block cipher that was "
        "adopted as a federal standard in 1977. It uses a 56-bit key and encrypts "
        "64-bit blocks. While now considered insecure, it's important historically."
    )
    key_type = "text"
    key_hint = "Enter exactly 8 characters for key"
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using DES. Returns base64 encoded ciphertext."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required. Install with: pip install pycryptodome")
        
        key = str(key)
        
        # Ensure key is exactly 8 bytes
        if len(key) < 8:
            key = key + '\x00' * (8 - len(key))
        key = key[:8].encode('utf-8')
        
        cipher = DES.new(key, DES.MODE_CBC)
        
        # Pad plaintext to multiple of 8 bytes
        plaintext_bytes = plaintext.encode('utf-8')
        padded = pad(plaintext_bytes, DES.block_size)
        
        # Encrypt
        ciphertext = cipher.encrypt(padded)
        
        # Return IV + ciphertext as base64
        result = base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
        return result
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt DES. Input is base64 encoded."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required. Install with: pip install pycryptodome")
        
        key = str(key)
        
        # Ensure key is exactly 8 bytes
        if len(key) < 8:
            key = key + '\x00' * (8 - len(key))
        key = key[:8].encode('utf-8')
        
        # Decode base64
        data = base64.b64decode(ciphertext)
        
        # Extract IV (first 8 bytes) and ciphertext
        iv = data[:8]
        encrypted = data[8:]
        
        cipher = DES.new(key, DES.MODE_CBC, iv=iv)
        
        # Decrypt and unpad
        decrypted = cipher.decrypt(encrypted)
        plaintext = unpad(decrypted, DES.block_size)
        
        return plaintext.decode('utf-8')
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if len(key) < 1:
            return False, "Key must have at least one character (will be padded to 8)"
        return True, ""
