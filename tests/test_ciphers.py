"""Comprehensive tests for all cipher implementations."""

import pytest
from cryptolab.ciphers import (
    CaesarCipher, AdditiveCipher, MultiplicativeCipher, AffineCipher,
    VigenereCipher, HillCipher, AutokeyCipher, PlayfairCipher,
    OTPCipher, VernamCipher, RailFenceCipher, ColumnarCipher,
    FeistelCipher, DESCipher, AESCipher, RSACipher,
    get_cipher, get_all_ciphers
)


class TestCaesarCipher:
    """Tests for Caesar cipher."""
    
    def test_encrypt_basic(self):
        cipher = CaesarCipher()
        assert cipher.encrypt("HELLO", 3) == "KHOOR"
    
    def test_encrypt_lowercase(self):
        cipher = CaesarCipher()
        assert cipher.encrypt("hello", 3) == "khoor"
    
    def test_encrypt_mixed_case(self):
        cipher = CaesarCipher()
        assert cipher.encrypt("Hello World", 3) == "Khoor Zruog"
    
    def test_decrypt_basic(self):
        cipher = CaesarCipher()
        assert cipher.decrypt("KHOOR", 3) == "HELLO"
    
    def test_roundtrip(self):
        cipher = CaesarCipher()
        original = "The Quick Brown Fox"
        encrypted = cipher.encrypt(original, 7)
        decrypted = cipher.decrypt(encrypted, 7)
        assert decrypted == original
    
    def test_validate_key_valid(self):
        assert CaesarCipher.validate_key(5)[0] is True
    
    def test_validate_key_invalid(self):
        assert CaesarCipher.validate_key(30)[0] is False


class TestAdditiveCipher:
    """Tests for Additive cipher."""
    
    def test_encrypt_basic(self):
        cipher = AdditiveCipher()
        assert cipher.encrypt("HELLO", 3) == "KHOOR"
    
    def test_decrypt_basic(self):
        cipher = AdditiveCipher()
        assert cipher.decrypt("KHOOR", 3) == "HELLO"
    
    def test_roundtrip(self):
        cipher = AdditiveCipher()
        original = "Testing Additive"
        for key in [0, 5, 13, 25]:
            encrypted = cipher.encrypt(original, key)
            decrypted = cipher.decrypt(encrypted, key)
            assert decrypted == original


class TestMultiplicativeCipher:
    """Tests for Multiplicative cipher."""
    
    def test_encrypt_basic(self):
        cipher = MultiplicativeCipher()
        result = cipher.encrypt("HELLO", 3)
        assert len(result) == 5
    
    def test_roundtrip(self):
        cipher = MultiplicativeCipher()
        original = "TESTMESSAGE"
        for key in [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
            encrypted = cipher.encrypt(original, key)
            decrypted = cipher.decrypt(encrypted, key)
            assert decrypted == original, f"Failed for key {key}"
    
    def test_validate_key_not_coprime(self):
        assert MultiplicativeCipher.validate_key(2)[0] is False
        assert MultiplicativeCipher.validate_key(13)[0] is False


class TestAffineCipher:
    """Tests for Affine cipher."""
    
    def test_encrypt_basic(self):
        cipher = AffineCipher()
        result = cipher.encrypt("HELLO", "5 8")
        assert result == "RCLLA"
    
    def test_decrypt_basic(self):
        cipher = AffineCipher()
        result = cipher.decrypt("RCLLA", "5 8")
        assert result == "HELLO"
    
    def test_roundtrip(self):
        cipher = AffineCipher()
        original = "ATTACKATDAWN"
        for a in [3, 5, 7, 11, 17]:
            for b in [0, 5, 10, 15]:
                key = f"{a} {b}"
                encrypted = cipher.encrypt(original, key)
                decrypted = cipher.decrypt(encrypted, key)
                assert decrypted == original, f"Failed for key {key}"
    
    def test_validate_key_not_coprime(self):
        assert AffineCipher.validate_key("4 5")[0] is False


class TestVigenereCipher:
    """Tests for Vigenère cipher."""
    
    def test_encrypt_basic(self):
        cipher = VigenereCipher()
        assert cipher.encrypt("HELLO", "KEY") == "RIJVS"
    
    def test_decrypt_basic(self):
        cipher = VigenereCipher()
        assert cipher.decrypt("RIJVS", "KEY") == "HELLO"
    
    def test_roundtrip(self):
        cipher = VigenereCipher()
        original = "ATTACKATDAWN"
        key = "LEMON"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_preserves_case(self):
        cipher = VigenereCipher()
        original = "Hello World"
        encrypted = cipher.encrypt(original, "KEY")
        decrypted = cipher.decrypt(encrypted, "KEY")
        assert decrypted == original


class TestHillCipher:
    """Tests for Hill cipher."""
    
    def test_encrypt_basic(self):
        cipher = HillCipher()
        result = cipher.encrypt("HELP", "3 3 2 5")
        assert len(result) == 4
    
    def test_roundtrip(self):
        cipher = HillCipher()
        original = "TEST"
        key = "3 3 2 5"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_roundtrip_longer(self):
        cipher = HillCipher()
        original = "HELLOWORLD"
        key = "5 17 4 15"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_validate_key_invalid_det(self):
        assert HillCipher.validate_key("2 4 6 8")[0] is False


class TestAutokeyCipher:
    """Tests for Autokey cipher."""
    
    def test_encrypt_basic(self):
        cipher = AutokeyCipher()
        result = cipher.encrypt("HELLO", "KEY")
        assert len(result) == 5
    
    def test_roundtrip(self):
        cipher = AutokeyCipher()
        original = "ATTACKATDAWN"
        key = "SECRET"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_preserves_case(self):
        cipher = AutokeyCipher()
        original = "Hello World"
        encrypted = cipher.encrypt(original, "KEY")
        decrypted = cipher.decrypt(encrypted, "KEY")
        assert decrypted == original


class TestPlayfairCipher:
    """Tests for Playfair cipher."""
    
    def test_encrypt_basic(self):
        cipher = PlayfairCipher()
        result = cipher.encrypt("HELLO", "KEYWORD")
        assert len(result) > 0
    
    def test_roundtrip_simple(self):
        cipher = PlayfairCipher()
        original = "HIDETHETREASURE"
        key = "MONARCHY"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        # Playfair may add padding, check core content
        assert decrypted.startswith("HIDE")


class TestOTPCipher:
    """Tests for One-Time Pad cipher."""
    
    def test_encrypt_basic(self):
        cipher = OTPCipher()
        result = cipher.encrypt("HELLO", "XMCKL")
        assert len(result) == 5
    
    def test_roundtrip(self):
        cipher = OTPCipher()
        original = "SECRET"
        key = "RANDOMKEY"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_key_too_short(self):
        cipher = OTPCipher()
        with pytest.raises(ValueError):
            cipher.encrypt("HELLO WORLD TEST", "KEY")


class TestVernamCipher:
    """Tests for Vernam cipher."""
    
    def test_encrypt_basic(self):
        cipher = VernamCipher()
        result = cipher.encrypt("HI", "K")
        assert len(result) > 0
    
    def test_roundtrip(self):
        cipher = VernamCipher()
        original = "Hello World!"
        key = "SECRETKEY"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_special_characters(self):
        cipher = VernamCipher()
        original = "Test@123!"
        key = "KEY"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original


class TestRailFenceCipher:
    """Tests for Rail Fence cipher."""
    
    def test_encrypt_basic(self):
        cipher = RailFenceCipher()
        result = cipher.encrypt("WEAREDISCOVERED", 3)
        assert "W" in result
    
    def test_roundtrip(self):
        cipher = RailFenceCipher()
        original = "WEAREDISCOVEREDFLEEATONCE"
        for rails in [2, 3, 4, 5]:
            encrypted = cipher.encrypt(original, rails)
            decrypted = cipher.decrypt(encrypted, rails)
            assert decrypted == original, f"Failed for {rails} rails"
    
    def test_validate_key(self):
        assert RailFenceCipher.validate_key(1)[0] is False
        assert RailFenceCipher.validate_key(3)[0] is True


class TestColumnarCipher:
    """Tests for Columnar Transposition cipher."""
    
    def test_encrypt_basic(self):
        cipher = ColumnarCipher()
        result = cipher.encrypt("HELLOWORLD", "KEY")
        assert len(result) >= 10
    
    def test_roundtrip(self):
        cipher = ColumnarCipher()
        original = "ATTACKATDAWNXXX"
        key = "ZEBRA"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert original in decrypted or decrypted.startswith(original[:10])


class TestFeistelCipher:
    """Tests for Feistel cipher."""
    
    def test_encrypt_basic(self):
        cipher = FeistelCipher()
        result = cipher.encrypt("Hello", "SECRET")
        assert len(result) > 0
    
    def test_roundtrip(self):
        cipher = FeistelCipher()
        original = "Test Message"
        key = "MySecretKey"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted.rstrip('\x00') == original


class TestDESCipher:
    """Tests for DES cipher."""
    
    def test_encrypt_basic(self):
        cipher = DESCipher()
        result = cipher.encrypt("Hello", "password")
        assert len(result) > 0
    
    def test_roundtrip(self):
        cipher = DESCipher()
        original = "Test Message for DES"
        key = "mykey123"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original


class TestAESCipher:
    """Tests for AES cipher."""
    
    def test_encrypt_basic(self):
        cipher = AESCipher()
        result = cipher.encrypt("Hello", "password")
        assert len(result) > 0
    
    def test_roundtrip_128(self):
        cipher = AESCipher()
        original = "Test Message for AES-128"
        key = "1234567890123456"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original
    
    def test_roundtrip_256(self):
        cipher = AESCipher()
        original = "Test Message for AES-256"
        key = "12345678901234567890123456789012"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original


class TestRSACipher:
    """Tests for RSA cipher."""
    
    def test_encrypt_basic(self):
        cipher = RSACipher()
        result = cipher.encrypt("Hello", "password123")
        assert len(result) > 0
    
    def test_roundtrip(self):
        cipher = RSACipher()
        original = "Test Message for RSA"
        key = "mypassword"
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        assert decrypted == original




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
        assert len(ciphers) == 16
        assert "caesar" in ciphers
        assert "aes" in ciphers
        assert "rsa" in ciphers
    
    def test_all_ciphers_have_required_attributes(self):
        ciphers = get_all_ciphers()
        for name, info in ciphers.items():
            assert "name" in info
            assert "description" in info
            assert "key_type" in info
            assert "key_hint" in info
