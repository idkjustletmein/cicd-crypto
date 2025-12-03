"""Playfair Cipher implementation."""

from .base import BaseCipher


class PlayfairCipher(BaseCipher):
    """
    Playfair Cipher - digraph substitution using a 5x5 key square.
    """
    
    name = "Playfair Cipher"
    description = (
        "The Playfair cipher encrypts pairs of letters (digraphs) using a 5x5 "
        "key square. It was invented by Charles Wheatstone in 1854 but named after "
        "Lord Playfair who promoted its use. It was used by the British in WWI and "
        "by the Australians in WWII."
    )
    key_type = "text"
    key_hint = "Enter keyword to generate 5x5 grid"
    strength = 5
    
    def _create_matrix(self, key: str) -> list[list[str]]:
        """Create the 5x5 Playfair matrix from the key."""
        key = key.upper().replace('J', 'I').replace(' ', '')
        seen = set()
        matrix_chars = []
        
        # Add unique key characters
        for char in key:
            if char.isalpha() and char not in seen:
                seen.add(char)
                matrix_chars.append(char)
        
        # Add remaining alphabet (I/J combined)
        for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if char not in seen:
                matrix_chars.append(char)
        
        # Create 5x5 matrix
        return [matrix_chars[i:i+5] for i in range(0, 25, 5)]
    
    def _find_position(self, matrix: list[list[str]], char: str) -> tuple[int, int]:
        """Find character position in matrix."""
        char = 'I' if char == 'J' else char
        for i, row in enumerate(matrix):
            if char in row:
                return i, row.index(char)
        raise ValueError(f"Character {char} not found in matrix")
    
    def _prepare_text(self, text: str) -> list[str]:
        """Prepare text for encryption (create digraphs)."""
        text = text.upper().replace('J', 'I').replace(' ', '')
        text = ''.join(c for c in text if c.isalpha())
        
        digraphs = []
        i = 0
        while i < len(text):
            if i + 1 >= len(text):
                digraphs.append(text[i] + 'X')
                i += 1
            elif text[i] == text[i + 1]:
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i] + text[i + 1])
                i += 2
        
        return digraphs
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Playfair cipher."""
        matrix = self._create_matrix(key)
        digraphs = self._prepare_text(plaintext)
        result = []
        
        for digraph in digraphs:
            r1, c1 = self._find_position(matrix, digraph[0])
            r2, c2 = self._find_position(matrix, digraph[1])
            
            if r1 == r2:  # Same row
                result.append(matrix[r1][(c1 + 1) % 5])
                result.append(matrix[r2][(c2 + 1) % 5])
            elif c1 == c2:  # Same column
                result.append(matrix[(r1 + 1) % 5][c1])
                result.append(matrix[(r2 + 1) % 5][c2])
            else:  # Rectangle
                result.append(matrix[r1][c2])
                result.append(matrix[r2][c1])
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Playfair cipher."""
        matrix = self._create_matrix(key)
        ciphertext = ciphertext.upper().replace(' ', '')
        ciphertext = ''.join(c for c in ciphertext if c.isalpha())
        
        digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        result = []
        
        for digraph in digraphs:
            r1, c1 = self._find_position(matrix, digraph[0])
            r2, c2 = self._find_position(matrix, digraph[1])
            
            if r1 == r2:  # Same row
                result.append(matrix[r1][(c1 - 1) % 5])
                result.append(matrix[r2][(c2 - 1) % 5])
            elif c1 == c2:  # Same column
                result.append(matrix[(r1 - 1) % 5][c1])
                result.append(matrix[(r2 - 1) % 5][c2])
            else:  # Rectangle
                result.append(matrix[r1][c2])
                result.append(matrix[r2][c1])
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO',
            'key': 'KEYWORD',
            'steps': [
                'Grid from KEYWORD: K E Y W O / R D A B C / F G H I L / M N P Q S / T U V X Z',
                'Split: HE LL O(X) → HE LX LO',
                'HE: H(row2,col2) E(row0,col1) → rectangle → swap cols → KH',
                'LX: L(row2,col4) X(row4,col3) → rectangle → swap cols → SZ',
                'LO: L(row2,col4) O(row0,col4) → same col → shift down → OY',
            ],
            'result': 'KHSZOY'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if not any(c.isalpha() for c in key):
            return False, "Key must contain at least one letter"
        return True, ""
