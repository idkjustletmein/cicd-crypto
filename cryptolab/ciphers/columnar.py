"""Columnar Transposition Cipher implementation."""

from .base import BaseCipher


class ColumnarCipher(BaseCipher):
    """
    Columnar Transposition Cipher - rearranges text by columns.
    Writes plaintext in rows under keyword, reads columns in alphabetical order.
    """
    
    name = "Columnar Transposition"
    description = (
        "The Columnar Transposition cipher writes the plaintext in rows under a "
        "keyword, then reads off columns in alphabetical order of the key letters. "
        "Widely used in WWI and WWII."
    )
    key_type = "text"
    key_hint = "Enter keyword (determines column order)"
    
    def _get_column_order(self, key: str) -> list:
        """Get column reading order based on alphabetical sort of key."""
        key = key.upper()
        # Create list of (original_index, char) sorted by (char, original_index)
        indexed = list(enumerate(key))
        sorted_indexed = sorted(indexed, key=lambda x: (x[1], x[0]))
        
        # Return positions in sorted order
        return [item[0] for item in sorted_indexed]
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Columnar Transposition cipher."""
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError("Key must contain at least one letter")
        
        # Remove spaces for processing
        text = plaintext.replace(' ', '').upper()
        num_cols = len(key)
        
        # Pad text to fill complete grid
        padding_needed = (num_cols - len(text) % num_cols) % num_cols
        text += 'X' * padding_needed
        
        # Create grid (list of rows)
        num_rows = len(text) // num_cols
        grid = []
        for i in range(num_rows):
            grid.append(list(text[i * num_cols:(i + 1) * num_cols]))
        
        # Read columns in key order
        column_order = self._get_column_order(key)
        result = []
        
        for col in column_order:
            for row in grid:
                result.append(row[col])
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Columnar Transposition cipher."""
        key = ''.join(c.upper() for c in str(key) if c.isalpha())
        if not key:
            raise ValueError("Key must contain at least one letter")
        
        text = ciphertext.replace(' ', '').upper()
        num_cols = len(key)
        num_rows = len(text) // num_cols
        
        if num_rows == 0:
            return text
        
        column_order = self._get_column_order(key)
        
        # Fill columns in key order
        columns = [''] * num_cols
        idx = 0
        
        for col in column_order:
            columns[col] = text[idx:idx + num_rows]
            idx += num_rows
        
        # Read rows
        result = []
        for row in range(num_rows):
            for col in range(num_cols):
                if row < len(columns[col]):
                    result.append(columns[col][row])
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        clean_key = ''.join(c for c in key if c.isalpha())
        if len(clean_key) < 2:
            return False, "Key must have at least 2 letters"
        return True, ""
