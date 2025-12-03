"""Tests for all cipher implementations."""

import pytest
from cryptolab.ciphers import (
    CaesarCipher, VigenereCipher, AutokeyCipher, OneTimePadCipher,
    HillCipher, AffineCipher, MultiplicativeCipher, PlayfairCipher,
    VernamCipher, RailFenceCipher, ColumnarCipher,
    get_cipher, get_all_ciphers
)


class TestCaesarCipher:
    """Tests for Caesar cipher."""
    
    def test_encrypt_basic(self):
        cipher = CaesarCipher()
        assert cipher.encrypt("HELLO", 3) == "KHOOR"
    
    def test_encrypt_with_spaces(self):
        cipher = CaesarCipher()
        assert cipher.encrypt("HELLO WORLD", 3) == "KHOOR ZRUOG"
    
    def test_decrypt_basic(self):
        cipher = CaesarCipher()
        assert cipher.decrypt("KHOOR", 3) == "HELLO"
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = CaesarCipher()
        original = "THE QUICK BROWN FOX"
        encrypted = cipher.encrypt(original, 7)
        decrypted = cipher.decrypt(encrypted, 7)
        assert decrypted == original
    
    def test_validate_key_valid(self):
        is_valid, msg = CaesarCipher.validate_key(5)
        assert is_valid is True
    
    def test_validate_key_invalid_range(self):
        is_valid, msg = CaesarCipher.validate_key(30)
        assert is_valid is False
    
    def test_validate_key_invalid_type(self):
        is_valid, msg = CaesarCipher.validate_key("abc")
        assert is_valid is False


class TestVigenereCipher:
    """Tests for Vigenère cipher."""
    
    def test_encrypt_basic(self):
        cipher = VigenereCipher()
        assert cipher.encrypt("HELLO", "KEY") == "RIJVS"
    
    def test_decrypt_basic(self):
        cipher = VigenereCipher()
        assert cipher.decrypt("RIJVS", "KEY") == "HELLO"
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = VigenereCipher()
        original = "ATTACKATDAWN"
        key = "LEMON"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_validate_key_valid(self):
        is_valid, msg = VigenereCipher.validate_key("SECRET")
        assert is_valid is True
    
    def test_validate_key_empty(self):
        is_valid, msg = VigenereCipher.validate_key("")
        assert is_valid is False


class TestAutokeyCipher:
    """Tests for Autokey cipher."""
    
    def test_encrypt_basic(self):
        cipher = AutokeyCipher()
        result = cipher.encrypt("HELLO", "KEY")
        assert len(result) == 5
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = AutokeyCipher()
        original = "TESTMESSAGE"
        key = "SECRET"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original


class TestOneTimePadCipher:
    """Tests for One-Time Pad cipher."""
    
    def test_encrypt_basic(self):
        cipher = OneTimePadCipher()
        result = cipher.encrypt("HELLO", "XMCKL")
        assert len(result) == 5
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = OneTimePadCipher()
        original = "SECRET"
        key = "ABCDEF"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_key_too_short(self):
        cipher = OneTimePadCipher()
        with pytest.raises(ValueError):
            cipher.encrypt("HELLO WORLD", "KEY")


class TestHillCipher:
    """Tests for Hill cipher."""
    
    def test_encrypt_basic(self):
        cipher = HillCipher()
        result = cipher.encrypt("HELP", "6 24 1 13")
        assert len(result) == 4
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = HillCipher()
        original = "TEST"
        key = "3 3 2 5"  # det = 15-6 = 9, gcd(9,26)=1
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_validate_key_valid(self):
        is_valid, msg = HillCipher.validate_key("3 3 2 5")
        assert is_valid is True
    
    def test_validate_key_invalid_det(self):
        is_valid, msg = HillCipher.validate_key("2 4 2 4")
        assert is_valid is False


class TestAffineCipher:
    """Tests for Affine cipher."""
    
    def test_encrypt_basic(self):
        cipher = AffineCipher()
        assert cipher.encrypt("HELLO", "5 8") == "RCLLA"
    
    def test_decrypt_basic(self):
        cipher = AffineCipher()
        assert cipher.decrypt("RCLLA", "5 8") == "HELLO"
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = AffineCipher()
        original = "TESTING"
        key = "7 3"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_validate_key_not_coprime(self):
        is_valid, msg = AffineCipher.validate_key("4 5")
        assert is_valid is False


class TestMultiplicativeCipher:
    """Tests for Multiplicative cipher."""
    
    def test_encrypt_basic(self):
        cipher = MultiplicativeCipher()
        result = cipher.encrypt("HELLO", 7)
        assert len(result) == 5
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = MultiplicativeCipher()
        original = "TESTMSG"
        key = 9
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_validate_key_not_coprime(self):
        is_valid, msg = MultiplicativeCipher.validate_key(13)
        assert is_valid is False


class TestPlayfairCipher:
    """Tests for Playfair cipher."""
    
    def test_encrypt_basic(self):
        cipher = PlayfairCipher()
        result = cipher.encrypt("HELLO", "KEYWORD")
        assert len(result) > 0
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = PlayfairCipher()
        original = "TESTMESSAGE"
        key = "SECRET"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        # Playfair may add padding X's, so check prefix
        assert decrypted.startswith("TEST") or "TEST" in decrypted


class TestVernamCipher:
    """Tests for Vernam cipher."""
    
    def test_encrypt_basic(self):
        cipher = VernamCipher()
        result = cipher.encrypt("HI", "K")
        assert len(result) > 0
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = VernamCipher()
        original = "SECRET"
        key = "MYKEY"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original


class TestRailFenceCipher:
    """Tests for Rail Fence cipher."""
    
    def test_encrypt_basic(self):
        cipher = RailFenceCipher()
        result = cipher.encrypt("HELLO WORLD", 3)
        assert "H" in result
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = RailFenceCipher()
        original = "WEAREDISCOVERED"
        key = 3
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_validate_key_too_small(self):
        is_valid, msg = RailFenceCipher.validate_key(1)
        assert is_valid is False


class TestColumnarCipher:
    """Tests for Columnar Transposition cipher."""
    
    def test_encrypt_basic(self):
        cipher = ColumnarCipher()
        result = cipher.encrypt("HELLO WORLD", "KEY")
        assert len(result) > 0
    
    def test_encrypt_decrypt_roundtrip(self):
        cipher = ColumnarCipher()
        original = "TESTMESSAGE"
        key = "CRYPTO"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        # May have padding
        assert original in decrypted or decrypted.startswith(original)


class TestCipherRegistry:
    """Tests for the cipher registry."""
    
    def test_get_cipher_exists(self):
        cipher_class = get_cipher("caesar")
        assert cipher_class is not None
        assert cipher_class.name == "Caesar Cipher"
    
    def test_get_cipher_not_exists(self):
        cipher_class = get_cipher("nonexistent")
        assert cipher_class is None
    
    def test_get_all_ciphers(self):
        ciphers = get_all_ciphers()
        assert len(ciphers) == 11
        assert "caesar" in ciphers
        assert "vigenere" in ciphers
        assert "hill" in ciphers
    
    def test_cipher_has_required_attributes(self):
        ciphers = get_all_ciphers()
        for name, info in ciphers.items():
            assert "name" in info
            assert "description" in info
            assert "key_type" in info
            assert "key_hint" in info
            assert "strength" in info


class TestCipherExamples:
    """Tests for cipher example methods."""
    
    def test_all_ciphers_have_examples(self):
        ciphers = [
            CaesarCipher, VigenereCipher, AutokeyCipher, OneTimePadCipher,
            HillCipher, AffineCipher, MultiplicativeCipher, PlayfairCipher,
            VernamCipher, RailFenceCipher, ColumnarCipher
        ]
        for cipher_class in ciphers:
            example = cipher_class.get_example()
            assert "plaintext" in example
            assert "key" in example
            assert "steps" in example
            assert "result" in example
            assert len(example["steps"]) > 0
