"""Base class for all ciphers."""

from abc import ABC, abstractmethod


class BaseCipher(ABC):
    """Abstract base class for cipher implementations."""
    
    name = "Base Cipher"
    description = "Base cipher class"
    key_type = "text"
    key_hint = "Enter key"
    
    @abstractmethod
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt the plaintext using the given key."""
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt the ciphertext using the given key."""
        pass
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        """Validate the key. Returns (is_valid, error_message)."""
        return True, ""
