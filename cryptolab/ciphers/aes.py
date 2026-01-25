"""AES Cipher implementation using PyCryptodome."""

import base64
from .base import BaseCipher

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class AESCipher(BaseCipher):
    """
    AES (Advanced Encryption Standard) - symmetric block cipher.
    Uses 128, 192, or 256-bit keys with 128-bit blocks.
    """
    
    name = "AES"
    description = (
        "AES (Advanced Encryption Standard) is the current standard for symmetric "
        "encryption, adopted in 2001. It supports key sizes of 128, 192, or 256 bits "
        "and encrypts 128-bit blocks. It's widely used in secure communications."
    )
    key_type = "text"
    key_hint = "Enter key (16, 24, or 32 chars for AES-128/192/256)"
    
    def _prepare_key(self, key: str) -> bytes:
        """Prepare key to valid AES length (16, 24, or 32 bytes)."""
        key_bytes = key.encode('utf-8')
        
        # Pad or truncate to nearest valid AES key size
        if len(key_bytes) <= 16:
            key_bytes = key_bytes.ljust(16, b'\x00')
        elif len(key_bytes) <= 24:
            key_bytes = key_bytes.ljust(24, b'\x00')
        else:
            key_bytes = key_bytes.ljust(32, b'\x00')[:32]
        
        return key_bytes
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using AES-CBC. Returns base64 encoded ciphertext."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required. Install with: pip install pycryptodome")
        
        key_bytes = self._prepare_key(str(key))
        
        cipher = AES.new(key_bytes, AES.MODE_CBC)
        
        # Pad plaintext to multiple of 16 bytes
        plaintext_bytes = plaintext.encode('utf-8')
        padded = pad(plaintext_bytes, AES.block_size)
        
        # Encrypt
        ciphertext = cipher.encrypt(padded)
        
        # Return IV + ciphertext as base64
        result = base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
        return result
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt AES. Input is base64 encoded."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required. Install with: pip install pycryptodome")
        
        key_bytes = self._prepare_key(str(key))
        
        # Decode base64
        data = base64.b64decode(ciphertext)
        
        # Extract IV (first 16 bytes) and ciphertext
        iv = data[:16]
        encrypted = data[16:]
        
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv)
        
        # Decrypt and unpad
        decrypted = cipher.decrypt(encrypted)
        plaintext = unpad(decrypted, AES.block_size)
        
        return plaintext.decode('utf-8')
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if len(key) < 1:
            return False, "Key must have at least one character"
        return True, ""
