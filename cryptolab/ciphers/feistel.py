"""Feistel Cipher implementation."""

from .base import BaseCipher


class FeistelCipher(BaseCipher):
    """
    Feistel Cipher - symmetric block cipher structure.
    Demonstrates the Feistel network used in DES and other ciphers.
    """
    
    name = "Feistel Cipher"
    description = (
        "The Feistel cipher is a symmetric structure used in many block ciphers "
        "including DES. It splits data into two halves and processes them through "
        "multiple rounds. The same structure is used for both encryption and decryption."
    )
    key_type = "text"
    key_hint = "Enter key (will be used to generate round keys)"
    
    def _string_to_bits(self, text: str) -> list:
        """Convert string to list of bits."""
        bits = []
        for char in text:
            for i in range(7, -1, -1):
                bits.append((ord(char) >> i) & 1)
        return bits
    
    def _bits_to_string(self, bits: list) -> str:
        """Convert list of bits to string."""
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                byte.extend([0] * (8 - len(byte)))
            value = sum(b << (7 - j) for j, b in enumerate(byte))
            if value > 0:
                chars.append(chr(value))
        return ''.join(chars)
    
    def _bits_to_hex(self, bits: list) -> str:
        """Convert bits to hex string."""
        hex_str = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                byte.extend([0] * (8 - len(byte)))
            value = sum(b << (7 - j) for j, b in enumerate(byte))
            hex_str.append(format(value, '02X'))
        return ''.join(hex_str)
    
    def _hex_to_bits(self, hex_str: str) -> list:
        """Convert hex string to bits."""
        bits = []
        hex_str = hex_str.replace(' ', '')
        for i in range(0, len(hex_str), 2):
            byte = int(hex_str[i:i+2], 16)
            for j in range(7, -1, -1):
                bits.append((byte >> j) & 1)
        return bits
    
    def _generate_round_keys(self, key: str, num_rounds: int) -> list:
        """Generate round keys from the main key."""
        key_bits = self._string_to_bits(key)
        # Extend or truncate key to 64 bits
        while len(key_bits) < 64:
            key_bits.extend(key_bits[:64 - len(key_bits)])
        key_bits = key_bits[:64]
        
        round_keys = []
        for i in range(num_rounds):
            # Simple key schedule: rotate and XOR with round number
            shift = (i + 1) * 4
            rotated = key_bits[shift:] + key_bits[:shift]
            # XOR with round number pattern
            round_key = rotated[:32]
            round_keys.append(round_key)
        
        return round_keys
    
    def _round_function(self, right_half: list, round_key: list) -> list:
        """The round function F(R, K)."""
        # Expand right half if needed
        expanded = right_half[:]
        while len(expanded) < len(round_key):
            expanded.extend(right_half)
        expanded = expanded[:len(round_key)]
        
        # XOR with round key
        result = [expanded[i] ^ round_key[i] for i in range(len(round_key))]
        
        # Simple S-box substitution (for demo purposes)
        for i in range(len(result)):
            if i % 4 == 0 and i + 3 < len(result):
                # Rotate 4-bit blocks
                result[i], result[i+1], result[i+2], result[i+3] = \
                    result[i+1], result[i+2], result[i+3], result[i]
        
        return result[:len(right_half)]
    
    def _feistel_rounds(self, bits: list, round_keys: list, decrypt: bool = False) -> list:
        """Perform Feistel rounds."""
        # Ensure even length
        if len(bits) % 2 != 0:
            bits.append(0)
        
        half_len = len(bits) // 2
        left = bits[:half_len]
        right = bits[half_len:]
        
        # Reverse round keys for decryption
        if decrypt:
            round_keys = round_keys[::-1]
        
        for round_key in round_keys:
            # Feistel round: L' = R, R' = L XOR F(R, K)
            f_result = self._round_function(right, round_key)
            
            # Ensure f_result matches left half length
            while len(f_result) < len(left):
                f_result.append(0)
            f_result = f_result[:len(left)]
            
            new_right = [left[i] ^ f_result[i] for i in range(len(left))]
            left = right
            right = new_right
        
        # Final swap
        return right + left
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using Feistel cipher. Returns hex string."""
        if not key:
            raise ValueError("Key is required")
        
        bits = self._string_to_bits(plaintext)
        
        # Pad to multiple of 64 bits (8 bytes)
        while len(bits) % 64 != 0:
            bits.append(0)
        
        round_keys = self._generate_round_keys(key, 16)
        
        # Process 64-bit blocks
        result_bits = []
        for i in range(0, len(bits), 64):
            block = bits[i:i+64]
            encrypted_block = self._feistel_rounds(block, round_keys, decrypt=False)
            result_bits.extend(encrypted_block)
        
        return self._bits_to_hex(result_bits)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using Feistel cipher. Input is hex string."""
        if not key:
            raise ValueError("Key is required")
        
        bits = self._hex_to_bits(ciphertext)
        round_keys = self._generate_round_keys(key, 16)
        
        # Process 64-bit blocks
        result_bits = []
        for i in range(0, len(bits), 64):
            block = bits[i:i+64]
            if len(block) < 64:
                block.extend([0] * (64 - len(block)))
            decrypted_block = self._feistel_rounds(block, round_keys, decrypt=True)
            result_bits.extend(decrypted_block)
        
        result = self._bits_to_string(result_bits)
        return result.rstrip('\x00')
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key is required"
        if len(key) < 1:
            return False, "Key must have at least one character"
        return True, ""
