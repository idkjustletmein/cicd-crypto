"""
CryptoLab Ciphers Package
Contains implementations of classical cryptographic ciphers.
"""

from .caesar import CaesarCipher
from .vigenere import VigenereCipher
from .autokey import AutokeyCipher
from .onetimepad import OneTimePadCipher
from .hill import HillCipher
from .affine import AffineCipher
from .multiplicative import MultiplicativeCipher
from .playfair import PlayfairCipher
from .vernam import VernamCipher
from .railfence import RailFenceCipher
from .columnar import ColumnarCipher

# Registry of all available ciphers
CIPHER_REGISTRY = {
    'caesar': CaesarCipher,
    'vigenere': VigenereCipher,
    'autokey': AutokeyCipher,
    'onetimepad': OneTimePadCipher,
    'hill': HillCipher,
    'affine': AffineCipher,
    'multiplicative': MultiplicativeCipher,
    'playfair': PlayfairCipher,
    'vernam': VernamCipher,
    'railfence': RailFenceCipher,
    'columnar': ColumnarCipher,
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
            'strength': cipher.strength,
        }
        for name, cipher in CIPHER_REGISTRY.items()
    }
