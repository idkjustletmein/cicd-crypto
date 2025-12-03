"""Rail Fence Cipher implementation."""

from .base import BaseCipher


class RailFenceCipher(BaseCipher):
    """
    Rail Fence Cipher - zigzag transposition cipher.
    """
    
    name = "Rail Fence Cipher"
    description = (
        "The Rail Fence cipher writes the message in a zigzag pattern across "
        "multiple 'rails' (rows), then reads off each rail in order. It's a "
        "simple transposition cipher that rearranges letters without substitution. "
        "Easy to break but historically used for quick message obfuscation."
    )
    key_type = "number"
    key_hint = "Enter number of rails (2-10)"
    strength = 2
    
    def encrypt(self, plaintext: str, key) -> str:
        """Encrypt using Rail Fence cipher."""
        rails = int(key)
        plaintext = plaintext.replace(' ', '').upper()
        
        if rails <= 1 or rails >= len(plaintext):
            return plaintext
        
        # Create the fence pattern
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for char in plaintext:
            fence[rail].append(char)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        
        return ''.join(''.join(rail) for rail in fence)
    
    def decrypt(self, ciphertext: str, key) -> str:
        """Decrypt using Rail Fence cipher."""
        rails = int(key)
        ciphertext = ciphertext.replace(' ', '').upper()
        n = len(ciphertext)
        
        if rails <= 1 or rails >= n:
            return ciphertext
        
        # Calculate characters per rail
        pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
        counts = [0] * rails
        for i in range(n):
            counts[pattern[i % len(pattern)]] += 1
        
        # Split ciphertext into rails
        fence = []
        idx = 0
        for count in counts:
            fence.append(list(ciphertext[idx:idx + count]))
            idx += count
        
        # Read off in zigzag pattern
        result = []
        indices = [0] * rails
        rail = 0
        direction = 1
        
        for _ in range(n):
            result.append(fence[rail][indices[rail]])
            indices[rail] += 1
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        
        return ''.join(result)
    
    @classmethod
    def get_example(cls) -> dict:
        return {
            'plaintext': 'HELLO WORLD',
            'key': '3',
            'steps': [
                'Write in zigzag with 3 rails:',
                'Rail 0: H . . . O . . . L .',
                'Rail 1: . E . L . W . R . D',
                'Rail 2: . . L . . . O . . .',
                'Read rails: HOL + ELWRD + LO',
            ],
            'result': 'HOLELWRDLO'
        }
    
    @classmethod
    def validate_key(cls, key) -> tuple[bool, str]:
        try:
            k = int(key)
            if k < 2:
                return False, "Number of rails must be at least 2"
            if k > 10:
                return False, "Number of rails should not exceed 10"
            return True, ""
        except (ValueError, TypeError):
            return False, "Key must be a number"
