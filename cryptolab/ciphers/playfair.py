"""Playfair Cipher implementation."""

from .base import BaseCipher


class PlayfairCipher(BaseCipher):
    """
    Playfair Cipher - digraph substitution using a 5x5 key square.
    Encrypts pairs of letters using position-based rules.
    """
    
    name = "Playfair Cipher"
    description = (
        "The Playfair cipher encrypts pairs of letters (digraphs) using a 5x5 "
        "key square. Invented by Charles Wheatstone in 1854. I and J share the "
        "same cell. Same-letter pairs are separated by X."
    )
    key_type = "text"
    key_hint = "Enter keyword to generate 5x5 grid"
    
    def _create_matrix(self, key: str) -> list:
        """Create the 5x5 Playfair matrix from the key."""
        key = key.upper().replace('J', 'I')
        
        # Build matrix with unique key letters first, then remaining alphabet
        seen = set()
        matrix_chars = []
        
        for char in key:
            if char.isalpha() and char not in seen:
                seen.add(char)
                matrix_chars.append(char)
        
        for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # No J
            if char not in seen:
                matrix_chars.append(char)
        
        # Create 5x5 matrix
        return [matrix_chars[i*5:(i+1)*5] for i in range(5)]
    
    def _find_position(self, matrix: list, char: str) -> tuple:
        """Find character position (row, col) in matrix."""
        char = 'I' if char == 'J' else char.upper()
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return row, col
        raise ValueError(f"Character {char} not found in matrix")
    
    def _prepare_plaintext(self, text: str) -> list:
        """Prepare plaintext for encryption - create digraphs."""
        # Remove non-alpha and convert to uppercase, replace J with I
        text = ''.join(c.upper() for c in text if c.isalpha()).replace('J', 'I')
        
        digraphs = []
        i = 0
        while i < len(text):
            if i + 1 >= len(text):
                # Last single character - pad with X
                digraphs.append(text[i] + 'X')
                i += 1
            elif text[i] == text[i + 1]:
                # Same letter pair - insert X between
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i] + text[i + 1])
                i += 2
        
        return digraphs
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Playfair cipher."""
        matrix = self._create_matrix(str(key))
        digraphs = self._prepare_plaintext(plaintext)
        result = []
        
        for digraph in digraphs:
            r1, c1 = self._find_position(matrix, digraph[0])
            r2, c2 = self._find_position(matrix, digraph[1])
            
            if r1 == r2:
                # Same row - shift right
                result.append(matrix[r1][(c1 + 1) % 5])
                result.append(matrix[r2][(c2 + 1) % 5])
            elif c1 == c2:
                # Same column - shift down
                result.append(matrix[(r1 + 1) % 5][c1])
                result.append(matrix[(r2 + 1) % 5][c2])
            else:
                # Rectangle - swap columns
                result.append(matrix[r1][c2])
                result.append(matrix[r2][c1])
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Playfair cipher."""
        matrix = self._create_matrix(str(key))
        
        # Clean ciphertext
        ciphertext = ''.join(c.upper() for c in ciphertext if c.isalpha()).replace('J', 'I')
        
        # Split into digraphs
        digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        result = []
        
        for digraph in digraphs:
            if len(digraph) < 2:
                break
            
            r1, c1 = self._find_position(matrix, digraph[0])
            r2, c2 = self._find_position(matrix, digraph[1])
            
            if r1 == r2:
                # Same row - shift left
                result.append(matrix[r1][(c1 - 1) % 5])
                result.append(matrix[r2][(c2 - 1) % 5])
            elif c1 == c2:
                # Same column - shift up
                result.append(matrix[(r1 - 1) % 5][c1])
                result.append(matrix[(r2 - 1) % 5][c2])
            else:
                # Rectangle - swap columns
                result.append(matrix[r1][c2])
                result.append(matrix[r2][c1])
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if not any(c.isalpha() for c in key):
            return False, "Key must contain at least one letter"
        return True, ""
