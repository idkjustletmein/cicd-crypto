"""Columnar Transposition Cipher implementation."""

from .base import BaseCipher


class ColumnarCipher(BaseCipher):
    """
    Columnar Transposition Cipher - rearranges text by columns.
    """
    
    name = "Columnar Transposition"
    description = (
        "The Columnar Transposition cipher writes the plaintext in rows under a "
        "keyword, then reads off columns in alphabetical order of the key letters. "
        "It was widely used in WWI and WWII, often combined with other ciphers for "
        "additional security."
    )
    key_type = "text"
    key_hint = "Enter keyword (determines column order)"
    strength = 4
    
    def _get_column_order(self, key: str) -> list[int]:
        """Get column reading order based on alphabetical sort of key."""
        key = key.upper()
        # Create list of (char, original_index) and sort alphabetically
        sorted_pairs = sorted(enumerate(key), key=lambda x: (x[1], x[0]))
        # Return the original indices in sorted order
        return [pair[0] for pair in sorted_pairs]
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Columnar Transposition cipher."""
        key = key.upper().replace(' ', '')
        plaintext = plaintext.upper().replace(' ', '')
        num_cols = len(key)
        
        # Pad plaintext if necessary
        padding_needed = (num_cols - len(plaintext) % num_cols) % num_cols
        plaintext += 'X' * padding_needed
        
        # Create grid
        num_rows = len(plaintext) // num_cols
        grid = [plaintext[i * num_cols:(i + 1) * num_cols] for i in range(num_rows)]
        
        # Read columns in key order
        column_order = self._get_column_order(key)
        result = []
        for col in column_order:
            for row in grid:
                result.append(row[col])
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Columnar Transposition cipher."""
        key = key.upper().replace(' ', '')
        ciphertext = ciphertext.upper().replace(' ', '')
        num_cols = len(key)
        num_rows = len(ciphertext) // num_cols
        
        column_order = self._get_column_order(key)
        
        # Fill columns in key order
        columns = [''] * num_cols
        idx = 0
        for col in column_order:
            columns[col] = ciphertext[idx:idx + num_rows]
            idx += num_rows
        
        # Read rows
        result = []
        for row in range(num_rows):
            for col in range(num_cols):
                result.append(columns[col][row])
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO WORLD',
            'key': 'KEY',
            'steps': [
                'Key order: K=2, E=1, Y=3 → read columns as 2,1,3',
                'Write under KEY:',
                'K E Y',
                'H E L',
                'L O W',
                'O R L',
                'D X X',
                'Read col E(1): EORX, col K(2): HLOD, col Y(3): LWLX',
            ],
            'result': 'EORXHLODLWLX'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        key_clean = key.replace(' ', '')
        if not key_clean.isalpha():
            return False, "Key must contain only letters"
        if len(key_clean) < 2:
            return False, "Key must be at least 2 characters"
        return True, ""
