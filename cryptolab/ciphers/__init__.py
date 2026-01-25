"""
CryptoLab Ciphers Package
Contains implementations of classical and modern cryptographic ciphers.
"""

from .caesar import CaesarCipher
from .additive import AdditiveCipher
from .multiplicative import MultiplicativeCipher
from .affine import AffineCipher
from .vigenere import VigenereCipher
from .hill import HillCipher
from .autokey import AutokeyCipher
from .playfair import PlayfairCipher
from .otp import OTPCipher
from .vernam import VernamCipher
from .railfence import RailFenceCipher
from .columnar import ColumnarCipher
from .feistel import FeistelCipher
from .des import DESCipher
from .aes import AESCipher
from .rsa import RSACipher
from .hashing import HashingCipher, SHA1Cipher

# Registry of all available ciphers
CIPHER_REGISTRY = {
    'caesar': CaesarCipher,
    'additive': AdditiveCipher,
    'multiplicative': MultiplicativeCipher,
    'affine': AffineCipher,
    'vigenere': VigenereCipher,
    'hill': HillCipher,
    'autokey': AutokeyCipher,
    'playfair': PlayfairCipher,
    'otp': OTPCipher,
    'vernam': VernamCipher,
    'railfence': RailFenceCipher,
    'columnar': ColumnarCipher,
    'feistel': FeistelCipher,
    'des': DESCipher,
    'aes': AESCipher,
    'rsa': RSACipher,
    'hashing': HashingCipher,
    'sha1': SHA1Cipher,
}


def get_cipher(name):
    """Get a cipher class by name."""
    return CIPHER_REGISTRY.get(name.lower())


def get_all_ciphers():
    """Get information about all available ciphers."""
    return {
        name: {
            'name': cipher.name,
            'description': cipher.description,
            'key_type': cipher.key_type,
            'key_hint': cipher.key_hint,
        }
        for name, cipher in CIPHER_REGISTRY.items()
    }
