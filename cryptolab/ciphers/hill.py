"""Hill Cipher implementation."""

from math import gcd
from .base import BaseCipher


class HillCipher(BaseCipher):
    """
    Hill Cipher - uses matrix multiplication for encryption.
    Encrypts blocks of letters using a key matrix.
    """
    
    name = "Hill Cipher"
    description = (
        "The Hill cipher uses linear algebra (matrix multiplication) to encrypt "
        "blocks of letters. The key is a square matrix that must be invertible "
        "modulo 26. Invented by Lester S. Hill in 1929."
    )
    key_type = "matrix"
    key_hint = "Enter 4 numbers for 2x2 matrix (e.g., '3 3 2 5')"
    
    # Pre-computed modular inverses mod 26
    MOD_INVERSES = {
        1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19,
        15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25
    }
    
    def _parse_key(self, key: str) -> list:
        """Parse key string into a 2x2 matrix."""
        numbers = [int(x) for x in str(key).split()]
        if len(numbers) != 4:
            raise ValueError("Key must be 4 numbers for a 2x2 matrix")
        return [[numbers[0], numbers[1]], [numbers[2], numbers[3]]]
    
    def _determinant(self, matrix: list) -> int:
        """Calculate determinant of 2x2 matrix."""
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    def _mod_inverse(self, a: int) -> int:
        """Get modular multiplicative inverse of a mod 26."""
        a = a % 26
        if a < 0:
            a += 26
        if a in self.MOD_INVERSES:
            return self.MOD_INVERSES[a]
        raise ValueError(f"No modular inverse for {a} mod 26")
    
    def _matrix_inverse(self, matrix: list) -> list:
        """Calculate the inverse of a 2x2 matrix mod 26."""
        det = self._determinant(matrix)
        det_mod = det % 26
        if det_mod < 0:
            det_mod += 26
        
        det_inv = self._mod_inverse(det_mod)
        
        # Adjugate matrix for 2x2: swap diagonal, negate off-diagonal
        adj = [
            [matrix[1][1], -matrix[0][1]],
            [-matrix[1][0], matrix[0][0]]
        ]
        
        # Multiply adjugate by determinant inverse mod 26
        inv = [
            [(det_inv * adj[0][0]) % 26, (det_inv * adj[0][1]) % 26],
            [(det_inv * adj[1][0]) % 26, (det_inv * adj[1][1]) % 26]
        ]
        
        return inv
    
    def _matrix_multiply(self, matrix: list, vector: list) -> list:
        """Multiply 2x2 matrix by 2x1 vector mod 26."""
        return [
            (matrix[0][0] * vector[0] + matrix[0][1] * vector[1]) % 26,
            (matrix[1][0] * vector[0] + matrix[1][1] * vector[1]) % 26
        ]
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Hill cipher."""
        matrix = self._parse_key(key)
        
        # Extract only letters and convert to uppercase
        clean = ''.join(c.upper() for c in plaintext if c.isalpha())
        
        # Pad if necessary
        if len(clean) % 2 != 0:
            clean += 'X'
        
        result = []
        for i in range(0, len(clean), 2):
            # Convert pair to numbers
            vector = [ord(clean[i]) - ord('A'), ord(clean[i+1]) - ord('A')]
            
            # Multiply by key matrix
            encrypted = self._matrix_multiply(matrix, vector)
            
            # Convert back to letters
            result.append(chr(encrypted[0] + ord('A')))
            result.append(chr(encrypted[1] + ord('A')))
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Hill cipher."""
        matrix = self._parse_key(key)
        inv_matrix = self._matrix_inverse(matrix)
        
        # Extract only letters and convert to uppercase
        clean = ''.join(c.upper() for c in ciphertext if c.isalpha())
        
        result = []
        for i in range(0, len(clean), 2):
            if i + 1 >= len(clean):
                break
            
            # Convert pair to numbers
            vector = [ord(clean[i]) - ord('A'), ord(clean[i+1]) - ord('A')]
            
            # Multiply by inverse matrix
            decrypted = self._matrix_multiply(inv_matrix, vector)
            
            # Convert back to letters
            result.append(chr(decrypted[0] + ord('A')))
            result.append(chr(decrypted[1] + ord('A')))
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        try:
            numbers = [int(x) for x in str(key).split()]
            if len(numbers) != 4:
                return False, "Key must be 4 numbers for a 2x2 matrix"
            
            matrix = [[numbers[0], numbers[1]], [numbers[2], numbers[3]]]
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det_mod = det % 26
            if det_mod < 0:
                det_mod += 26
            
            if det_mod == 0:
                return False, "Matrix determinant cannot be 0 mod 26"
            if gcd(det_mod, 26) != 1:
                return False, f"Determinant ({det_mod}) must be coprime with 26"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be 4 space-separated numbers"
