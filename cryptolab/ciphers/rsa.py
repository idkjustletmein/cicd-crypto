"""RSA Cipher implementation using PyCryptodome."""

import base64
import hashlib
from .base import BaseCipher

try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    from Crypto.Random import get_random_bytes
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class RSACipher(BaseCipher):
    """
    RSA - asymmetric public-key cryptosystem.
    Uses key pairs for encryption/decryption.
    """
    
    name = "RSA"
    description = (
        "RSA is an asymmetric cryptosystem using public/private key pairs. "
        "For this demo, enter a password to generate a deterministic key pair. "
        "In real applications, keys are generated separately and stored securely."
    )
    key_type = "text"
    key_hint = "Enter password (generates key pair for demo)"
    
    # Cache for generated keys to ensure encrypt/decrypt use same key
    _key_cache = {}
    
    def _generate_key_pair(self, password: str):
        """Generate a deterministic RSA key pair from a password."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required")
        
        # Check cache first
        if password in self._key_cache:
            return self._key_cache[password]
        
        # Create deterministic seed from password
        seed = hashlib.sha256(password.encode()).digest()
        
        # Use seed to create deterministic random generator
        # We'll use a simple approach: generate key with fixed randomness
        import random
        random.seed(int.from_bytes(seed, 'big'))
        
        # Generate RSA key with deterministic randomness
        # Note: This is NOT cryptographically secure for production!
        # For demo purposes only.
        
        # Find two large primes deterministically
        def is_prime(n, k=10):
            if n < 2:
                return False
            if n == 2 or n == 3:
                return True
            if n % 2 == 0:
                return False
            r, d = 0, n - 1
            while d % 2 == 0:
                r += 1
                d //= 2
            for _ in range(k):
                a = random.randrange(2, n - 1)
                x = pow(a, d, n)
                if x == 1 or x == n - 1:
                    continue
                for _ in range(r - 1):
                    x = pow(x, 2, n)
                    if x == n - 1:
                        break
                else:
                    return False
            return True
        
        def gen_prime(bits):
            while True:
                n = random.getrandbits(bits)
                n |= (1 << bits - 1) | 1  # Ensure it's odd and has right bit length
                if is_prime(n):
                    return n
        
        # Generate 1024-bit primes for 2048-bit RSA
        p = gen_prime(1024)
        q = gen_prime(1024)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        
        # Calculate d (modular inverse of e mod phi)
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, d, _ = extended_gcd(e, phi)
        d = d % phi
        
        # Construct RSA key
        key = RSA.construct((n, e, d, p, q))
        
        # Cache the key
        self._key_cache[password] = key
        
        return key
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt using RSA public key. Returns base64 encoded ciphertext."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required. Install with: pip install pycryptodome")
        
        rsa_key = self._generate_key_pair(str(key))
        
        cipher = PKCS1_OAEP.new(rsa_key.publickey())
        
        plaintext_bytes = plaintext.encode('utf-8')
        
        # RSA can only encrypt limited data size
        # Max size for 2048-bit key with OAEP is about 190 bytes
        max_chunk_size = 190
        chunks = []
        
        for i in range(0, len(plaintext_bytes), max_chunk_size):
            chunk = plaintext_bytes[i:i + max_chunk_size]
            encrypted_chunk = cipher.encrypt(chunk)
            chunks.append(encrypted_chunk)
        
        # Combine chunks with length prefixes
        result = b''
        for chunk in chunks:
            result += len(chunk).to_bytes(2, 'big') + chunk
        
        return base64.b64encode(result).decode('utf-8')
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt using RSA private key. Input is base64 encoded."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required. Install with: pip install pycryptodome")
        
        rsa_key = self._generate_key_pair(str(key))
        
        cipher = PKCS1_OAEP.new(rsa_key)
        
        # Decode base64
        data = base64.b64decode(ciphertext)
        
        # Decrypt chunks
        plaintext_chunks = []
        i = 0
        while i < len(data):
            chunk_len = int.from_bytes(data[i:i+2], 'big')
            i += 2
            chunk = data[i:i + chunk_len]
            i += chunk_len
            
            decrypted_chunk = cipher.decrypt(chunk)
            plaintext_chunks.append(decrypted_chunk)
        
        return b''.join(plaintext_chunks).decode('utf-8')
    
    @classmethod
    def validate_key(cls, key) -> tuple:
        if not key or not isinstance(key, str):
            return False, "Key/password is required"
        if len(key) < 4:
            return False, "Password should be at least 4 characters"
        return True, ""
