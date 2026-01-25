"""Rail Fence Cipher implementation."""

from .base import BaseCipher


class RailFenceCipher(BaseCipher):
    """
    Rail Fence Cipher - zigzag transposition cipher.
    Writes message in zigzag across multiple rails, then reads off each rail.
    """
    
    name = "Rail Fence Cipher"
    description = (
        "The Rail Fence cipher writes the message in a zigzag pattern across "
        "multiple 'rails' (rows), then reads off each rail in order. It's a "
        "transposition cipher that rearranges letters without substitution."
    )
    key_type = "number"
    key_hint = "Enter number of rails (2-10)"
    
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt using Rail Fence cipher."""
        rails = int(key)
        
        # Remove spaces for cleaner output
        text = plaintext.replace(' ', '')
        
        if rails <= 1 or rails >= len(text):
            return text
        
        # Create fence structure
        fence = [[] for _ in range(rails)]
        
        rail = 0
        direction = 1  # 1 = down, -1 = up
        
        for char in text:
            fence[rail].append(char)
            
            # Change direction at top or bottom rail
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            
            rail += direction
        
        # Read off each rail
        return ''.join(''.join(rail) for rail in fence)
    
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt using Rail Fence cipher."""
        rails = int(key)
        text = ciphertext.replace(' ', '')
        n = len(text)
        
        if rails <= 1 or rails >= n:
            return text
        
        # Calculate the length of each rail
        rail_lengths = [0] * rails
        rail = 0
        direction = 1
        
        for _ in range(n):
            rail_lengths[rail] += 1
            
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            
            rail += direction
        
        # Split ciphertext into rails
        fence = []
        idx = 0
        for length in rail_lengths:
            fence.append(list(text[idx:idx + length]))
            idx += length
        
        # Read in zigzag pattern
        result = []
        rail_indices = [0] * rails
        rail = 0
        direction = 1
        
        for _ in range(n):
            result.append(fence[rail][rail_indices[rail]])
            rail_indices[rail] += 1
            
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            
            rail += direction
        
        return ''.join(result)
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        try:
            k = int(key)
            if k < 2:
                return False, "Number of rails must be at least 2"
            if k > 10:
                return False, "Number of rails should not exceed 10"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be a number"
