"""Hill Cipher implementation."""

import numpy as np
from .base import BaseCipher


class HillCipher(BaseCipher):
    """
    Hill Cipher - uses matrix multiplication for encryption.
    """
    
    name = "Hill Cipher"
    description = (
        "The Hill cipher uses linear algebra (matrix multiplication) to encrypt "
        "blocks of letters. The key is a square matrix that must be invertible "
        "modulo 26. It was invented by Lester S. Hill in 1929 and was the first "
        "polygraphic cipher practical for more than 3 symbols."
    )
    key_type = "matrix"
    key_hint = "Enter 4 numbers for 2x2 matrix (e.g., '6 24 1 13')"
    strength = 6
    
    def _parse_key(self, key: str) -> np.ndarray:
        """Parse key string into a 2x2 matrix."""
        numbers = [int(x) for x in key.split()]
        if len(numbers) != 4:
            raise ValueError("Key must be 4 numbers for a 2x2 matrix")
        return np.array(numbers).reshape(2, 2)
    
    def _mod_inverse(self, a: int, m: int = 26) -> int:
        """Find modular multiplicative inverse."""
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"No modular inverse for {a} mod {m}")
    
    def _matrix_mod_inverse(self, matrix: np.ndarray) -> np.ndarray:
        """Find modular inverse of a 2x2 matrix."""
        det = int(round(np.linalg.det(matrix))) % 26
        det_inv = self._mod_inverse(det, 26)
        
        # Adjugate matrix for 2x2
        adj = np.array([
            [matrix[1, 1], -matrix[0, 1]],
            [-matrix[1, 0], matrix[0, 0]]
        ])
        
        return (det_inv * adj) % 26
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Hill cipher."""
        matrix = self._parse_key(key)
        
        # Prepare plaintext
        clean = ''.join(c for c in plaintext.upper() if c.isalpha())
        if len(clean) % 2 != 0:
            clean += 'X'  # Padding
        
        result = []
        for i in range(0, len(clean), 2):
            pair = np.array([ord(clean[i]) - ord('A'), ord(clean[i+1]) - ord('A')])
            encrypted = np.dot(matrix, pair) % 26
            result.append(chr(int(encrypted[0]) + ord('A')))
            result.append(chr(int(encrypted[1]) + ord('A')))
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Hill cipher."""
        matrix = self._parse_key(key)
        inv_matrix = self._matrix_mod_inverse(matrix)
        
        clean = ''.join(c for c in ciphertext.upper() if c.isalpha())
        
        result = []
        for i in range(0, len(clean), 2):
            pair = np.array([ord(clean[i]) - ord('A'), ord(clean[i+1]) - ord('A')])
            decrypted = np.dot(inv_matrix, pair) % 26
            result.append(chr(int(round(decrypted[0])) + ord('A')))
            result.append(chr(int(round(decrypted[1])) + ord('A')))
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELP',
            'key': '6 24 1 13',
            'steps': [
                'Matrix K = [[6, 24], [1, 13]]',
                'HE → [7, 4] × K = [7×6+4×1, 7×24+4×13] mod 26',
                '[46, 220] mod 26 = [20, 12] → UM',
                'LP → [11, 15] × K = [81, 459] mod 26',
                '[81, 459] mod 26 = [3, 17] → DR',
            ],
            'result': 'UMDR'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        try:
            numbers = [int(x) for x in key.split()]
            if len(numbers) != 4:
                return False, "Key must be 4 numbers for a 2x2 matrix"
            matrix = np.array(numbers).reshape(2, 2)
            det = int(round(np.linalg.det(matrix))) % 26
            if det == 0:
                return False, "Matrix determinant cannot be 0"
            # Check if determinant is coprime with 26
            from math import gcd
            if gcd(det, 26) != 1:
                return False, "Matrix determinant must be coprime with 26"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be 4 space-separated numbers"
