"""Base class for all ciphers."""

from abc import ABC, abstractmethod


class BaseCipher(ABC):
    """Abstract base class for cipher implementations."""
    
    name = "Base Cipher"
    description = "Base cipher class"
    key_type = "text"  # 'text', 'number', 'matrix', etc.
    key_hint = "Enter key"
    strength = 1  # 1-10 scale
    
    @abstractmethod
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt the plaintext using the given key."""
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt the ciphertext using the given key."""
        pass
    
    @classmethod
    def get_example(cls) -> dict:
        """Return a step-by-step example of how the cipher works."""
        return {
            'plaintext': 'HELLO',
            'key': 'KEY',
            'steps': ['Step 1', 'Step 2'],
            'result': 'ENCRYPTED'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        """Validate the key. Returns (is_valid, error_message)."""
        return True, ""
